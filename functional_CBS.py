import cbsodata
import pandas as pd
import sqlalchemy
from credentials import login,database
cijfers_buurten_en_wijken = {'BuurtenenWijken2015':'83220NED',
                             'BuurtenenWijken2016':'83487NED',
                             'BuurtenenWijken2017':'83765NED',
                             'BuurtenenWijken2018':'84286NED'}
## HERE WE CONNECT TO THE DATABASE AND THEN WRITE THE DATA INTO THE DATABASE.
HOST = database['host']
DB = database['DB']
USER = login['user']
PASSWORD = login['password']

#this function translates the column names, it takes away the numbering, i.e.
# codering_3 becomes codering
def translator(string):
    exceptions = ['Appartement','VrijstaandeWoning','TweeOnderEenKapWoning',
                 'Hoekwoning','Tussenwoning','Huurwoning','EigenWoning']
    for x in exceptions:
        if x in string:
            return string
    split = string.split('_')
    if len(string.split('_')) == 1:
        return split[0]
    else:
        return '_'.join(split[:-1])

#This function is used to download the data from CBS and make it into a desired
#dataframe.
def process_data(CBS_codering):
    data = cbsodata.get_data(CBS_codering)
    collecting = {}
    for row in reversed(data):
        collecting[int('1'+ row['Codering_3'][2:])] = row
        row['Perioden'] = 2015
        row['Gemeentenaam_1'] = row['Gemeentenaam_1'].strip()
        row['SoortRegio_2'] = row['SoortRegio_2'].strip()
    df = pd.DataFrame.from_dict(collecting, orient='index', dtype=None)
    df.rename(columns = translator,inplace = True) 
    return df


engine = sqlalchemy.create_engine(
        'mysql://{0}:{1}@{2}/{3}'.format(USER,PASSWORD,HOST,DB))
dataset = {}
#here the actually work is done, by calling the functions from above for all
#datasets.
for x,y in cijfers_buurten_en_wijken.items():
    print('downloading data buurten en wijken from {}'.format(x))
    data = process_data(y)
    dataset[x] = data
    conn = engine.connect()
    data.to_sql(con= conn, name=x, if_exists='replace')    
    conn.close()

