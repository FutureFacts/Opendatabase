import pandas as pd
import sqlalchemy
from credentials import login,database
from databronnen import cijfers_buurten_en_wijken

## HERE THE CREDENTIALS ARE ASSIGNED 
HOST = database['host']
DB = database['DB']
USER = login['user']
PASSWORD = login['password']

year =  sorted([x for x in cijfers_buurten_en_wijken.keys()
                if 'Buurten' in  x])[-1][-4:]
vertaal_recent = 'VERTAAL_' + year
jongeren_recent = sorted([x for x in cijfers_buurten_en_wijken.keys()
                   if 'jongeren' in  x])[-1]
wmo_recent = sorted([x for x in cijfers_buurten_en_wijken.keys()
                     if 'wmo' in x])[-1]
sovo_recent = sorted([x for x in cijfers_buurten_en_wijken.keys()
                     if 'sociale_voorzieningen' in x])[-1]
leeftijd_recent = sorted([x for x in cijfers_buurten_en_wijken.keys()
                     if 'leeftijd' in x])[-1]

## HERE WE CONNECT TO THE DATABASE, USING SQL ALCHEMY.
engine = sqlalchemy.create_engine(
        'mysql://{0}:{1}@{2}/{3}'.format(USER,PASSWORD,HOST,DB))
dataset = {}
conn = engine.connect()
with open('./sql_statements/join_tables') as file:
    commands = file.read().split(';')
    for command in commands:
        command = command.format(jongeren_recent = jongeren_recent,
                                 wmo_recent = wmo_recent,
                                 sovo_recent = sovo_recent,
                                 leeftijd_recent = leeftijd_recent,
                                 vertaal_recent = vertaal_recent)
        print(conn.execute(command))

