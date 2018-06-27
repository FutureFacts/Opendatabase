#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 11:56:18 2018

@author: daniel.van.der.zee
"""

import cbsodata
import pandas as pd
import sqlalchemy
import urllib
from credentials import login,database

# Database Connection
HOST = database['host']
DB = database['DB']
USER = login['user']
PASSWORD = login['password']
DRIVER = "{ODBC Driver 17 for SQL Server}"

params = urllib.parse.quote_plus("DRIVER="+DRIVER+";SERVER="+HOST+";DATABASE="+DB+";UID="+USER+";PWD="+PASSWORD)
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

# Import CBS data
raw_data_2015 = cbsodata.get_data('83220NED')

wijk_data = [rij for rij in raw_data_2015 if 'Wijk' in rij['SoortRegio_2']]
for wijk in wijk_data:
    wijk['Gemeentenaam_1'] = wijk['Gemeentenaam_1'].strip()

result2015 = pd.DataFrame.from_dict(wijk_data, orient='columns' , dtype=None)

# Write to DB
result2015.to_sql(con= engine, name='wijken', if_exists='replace')
