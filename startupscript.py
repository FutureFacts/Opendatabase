import pandas as pd
import cbsodata
import sqlalchemy
from credentials import login, database
from process_functions.table_functions import (translator,
                                               process_data_buurten)
from databronnen import cijfers_buurten_en_wijken

BuurtenenWijken = {key:item for key,item in cijfers_buurten_en_wijken.items()
                   if 'BuurtenenWijken' in key}

## HERE WE CONNECT TO THE DATABASE
HOST = database['host']
DB = database['DB']
USER = login['user']
PASSWORD = login['password']
engine = sqlalchemy.create_engine(
        'mysql://{0}:{1}@{2}/{3}'.format(USER,PASSWORD,HOST,DB))

conn = engine.connect()
for name,item in BuurtenenWijken.items():
    source = item[0]
    function = item[1]
    data = function(source,name)
    vertaaltabel = data[['Gemeentenaam','WijkenEnBuurten','SoortRegio','Codering']]
    vertaaltabel['MMR_indeling'] = vertaaltabel['Codering']
    vertaaltabel['soort_regio_nieuwe_indeling'] = vertaaltabel['SoortRegio']
    vertaaltabel['WijkenEnBuurten_nieuwe_indeling'] = \
                            vertaaltabel['WijkenEnBuurten']
    table_name = 'VERTAAL_' + name[-4:]
    vertaaltabel.to_sql(con=conn, name=table_name,
                        if_exists='replace')
