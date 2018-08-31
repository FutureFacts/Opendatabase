import cbsodata
import pandas as pd
import sqlalchemy
from credentials import login,database
from table_functions import process_data_buurten
cijfers_buurten_en_wijken = {'BuurtenenWijken2015':'83220NED',
                             'BuurtenenWijken2016':'83487NED',
                             'BuurtenenWijken2017':'83765NED',
                             'BuurtenenWijken2018':'84286NED'}
## HERE THE CREDENTIALS ARE ASSIGNED 
HOST = database['host']
DB = database['DB']
USER = login['user']
PASSWORD = login['password']

#this function translates the column names, it takes away the numbering, i.e.
# codering_3 becomes codering

#This function is used to download the data from CBS and make it into a desired
#dataframe.
## HERE WE CONNECT TO THE DATABASE, USING SQL ALCHEMY.
engine = sqlalchemy.create_engine(
        'mysql://{0}:{1}@{2}/{3}'.format(USER,PASSWORD,HOST,DB))
dataset = {}
#here the actually work is done, by calling the functions from above for all
#datasets.
for x,y in cijfers_buurten_en_wijken.items():
    print('downloading data buurten en wijken from {}'.format(x))
    data = process_data_buurten(y)
    print(data.iloc[1])
    dataset[x] = data
    conn = engine.connect()
    data.to_sql(con= conn, name=x, if_exists='replace')    
    conn.close()

