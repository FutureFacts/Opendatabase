import os
import sqlalchemy
import pandas as pd
from credentials import login, database


HOST = database['host']
DB = database['DB']
USER = login['user']
PASSWORD = login['password']
engine = sqlalchemy.create_engine(
        'mysql://{0}:{1}@{2}/{3}'.format(USER,PASSWORD,HOST,DB))

conn = engine.connect()
translation = {'Wijk': 'WK',
               'Gemeente': 'GM',
               'Buurt': 'BU'
              }
               

walker = os.walk('./Vertaling_wijken/')
next(walker)
years = {}
for directory,_, files in walker:
    print(directory,files)
    year = [directory + '/' + x for x in files if x[-4:] == 'xlsx']
    print(year)
    years[directory[-4:]] = year

def update_dataframe(df,data):
    for index, row in data.iterrows():
        select = df['Codering'].map(lambda x: x.rstrip()) == row['Wijkcode']
        type_wijk = translation[row['SoortRegio'].strip()] 
        gemeente = ' (' + df.loc[select].iloc[0]['Gemeentenaam'] + ')'
        df.loc[select,['MMR_indeling',
                       'soort_regio_nieuwe_indeling',
                       'WijkenEnBuurten_nieuwe_indeling'
                      ]
              ] = (type_wijk + ' ' + row['MMR-wijk'] + gemeente ,
                   row['SoortRegio'],
                   row['MMR-wijk']
                  )    
    return df

for year in years.keys():
    table_name =  'VERTAAL_' + year
    SQL_statement = "SELECT * FROM " + DB + '.' + table_name
    df = pd.read_sql(SQL_statement,index_col='index',con=conn)
    for gemeente in years[year]:
        data = pd.read_excel(gemeente)
        df = update_dataframe(df,data)
    df.to_sql(con = conn, name = table_name,
              if_exists = 'replace')
