#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 14:09:14 2018

@author: daniel.van.der.zee
"""

import pandas as pd
import sqlalchemy

# Remove when put into function
# Function argument
arg = "Amsterdam"

# DB Credentials
login = {
    'user': 'futurefacts',
    'password': 'futurefacts'
}

database = {
    'host' : "cbsdatabase.czs4btkv2yrb.eu-central-1.rds.amazonaws.com",
    'DB' : 'DatabaseCBS'
}

__HOST = database['host']
__DB = database['DB']
__USER = login['user']
__PASSWORD = login['password']

# Connect to DB
engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                           format(__USER, __PASSWORD, __HOST, 
                                                  __DB))
connection = engine.connect()

# Collect metadata
metadata = sqlalchemy.MetaData(bind = connection)
metadata.reflect(bind = connection)
cols = metadata.tables['wijken'].columns

# Create query
query = sqlalchemy.select(['*']).where(cols.Gemeentenaam_1 == arg)

# Execute query and create dataframe
data = pd.read_sql(query, query.bind)

# Close DB connection
connection.close()

# Save to Excel
writer = pd.ExcelWriter('output_test.xlsx', engine = 'openpyxl')
data.to_excel(writer,sheet_name = 'Data')
writer.save()

