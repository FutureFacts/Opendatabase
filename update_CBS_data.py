import cbsodata
import pandas as pd
import sqlalchemy
from credentials import login,database
from process_functions.table_functions import (process_data_buurten,
                             process_data_jongeren, 
                             process_data_wmo,
                             process_data_sociale_voorzieningen,
                             process_data_gezondheidsmonitor)
from process_functions.combine import list_combine
from databronnen import cijfers_buurten_en_wijken

## HERE THE CREDENTIALS ARE ASSIGNED 
HOST = database['host']
DB = database['DB']
USER = login['user']
PASSWORD = login['password']


## HERE WE CONNECT TO THE DATABASE, USING SQL ALCHEMY.
engine = sqlalchemy.create_engine(
        'mysql://{0}:{1}@{2}/{3}'.format(USER,PASSWORD,HOST,DB))
dataset = {}
#here the actually work is done, by calling the functions from above for all
#datasets in cijfers_buurten_en_wijken.
for name,(identifier,function) in cijfers_buurten_en_wijken.items():
    print('downloading data buurten en wijken from {}'.format(name))
    data = function(identifier,name)
    dataset[name] = data
    print(data.head(2))
    conn = engine.connect()
    data.to_sql(con= conn, name=name, if_exists='replace')    
    conn.execute("CREATE INDEX idx_Codering \
                  ON CBS.{} (Codering(10))".format(name)) 
    conn.close()

## CREATE THE MOST RECENT TABLE FOR BUURTEN EN WIJKEN
Buurtenenwijken = {name:df for name,df in dataset.items() if
                   'BuurtenenWijken' in name}
most_recent,source = list_combine(Buurtenenwijken)
conn = engine.connect()
most_recent.to_sql(con= conn, name='BuurtenenWijken_most_recent', if_exists='replace')
source.to_sql(con= conn, name='source_BuurtenenWijken_most_recent', if_exists='replace')

