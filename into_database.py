import cbsodata
import pandas as pd
import sqlalchemy
from credentials import login, database

raw_data_2015 = cbsodata.get_data('83220NED')

wijk_data = [rij for rij in raw_data_2015 if 'Wijk' in rij['SoortRegio_2']]
for wijk in wijk_data:
    wijk['Gemeentenaam_1'] = wijk['Gemeentenaam_1'].strip()

result2015 = pd.DataFrame.from_dict(wijk_data, orient='columns' , dtype=None)

HOST = database['host']
DB = database['DB']
USER = login['user']
PASSWORD = login['password']

connection = sqlalchemy.create_engine(
        'mssql+pyodbc://{0}:{1}@{2}/{3}?driver=SQL+Server+Native+Client+11.0'.
                                           format(USER, PASSWORD,
                                                  HOST, DB))

result2015.to_sql(con= connection, name='wijken', if_exists='replace')


result2015
