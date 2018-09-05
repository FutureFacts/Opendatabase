import cbsodata
import pandas as pd
import sqlalchemy
from credentials import login,database
from table_functions import (process_data_buurten,
                             process_data_jongeren, 
                             process_data_wmo,
                             process_data_sociale_voorzieningen,
                             process_data_gezondheidsmonitor)
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
    data = function(identifier)
    dataset[name] = data
    conn = engine.connect()
    data.to_sql(con= conn, name=name, if_exists='replace')    
    conn.close()

