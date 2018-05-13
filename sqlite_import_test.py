# Importing libraries
import sqlite3
import pandas as pd
import requests


# pull JWT
url_JWT = 'https://auth.opensensors.com/auth/login'
headers_JWT = { 'x-api-key': 'UoheJ3fp0w7CJisPi26NzNOw2rEPyMj67ovksMo1' }
API_access_token = requests.get(url_JWT, headers = headers_JWT, timeout = 1000).json()

# pulling data from opensensors api
url_GPM = 'https://api.opensensors.com/getProjectMessages';
headers_GPM = { 'Authorization': API_access_token.get('jwtToken') }
parameters = {'fromDate': '2018-02-02',
           'toDate': '2018-02-03',
           'projectUri': 'zaha-hadid',
           'size': '500',
           'type': 'modcamHeatmap',
           'cursor': ''}

os_data_request = requests.get(url_GPM, headers = headers_GPM, params = parameters).json()

# create sqlite database
from os_helper import create_connection
create_connection("os_reading_AUB.sqlite")

# create table in database

# 1. creating sqlite task
table_name = str(os_data_request["nextCursor"])

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS """ + table_name + """ (
                                        items integer PRIMARY KEY,
                                        lastCursor text NOT NULL,
                                        nextCursor text,
                                        total text
                                    ); """





 
"""
# heatmaps = os_data_request['items'][0]['heatmap']
# data = pd.DataFrame.from_dict(os_data_request)
# import json
# decoded = json.loads(os_data_request.encoding)

# connect to database
table_name = 'Observations'
col_name_0 = 'time'
col_name_1 = 'x'
col_name_2 = 'y'
col_name_3 = 'value'

conn = sqlite3.connect('AUBsmall_Col.sqlite')
dataset = pd.read_sql_query('select * from Observations;', conn)
for v in range (0, len(os_data_request['items'][0]['heatmap'])):        
    conn.execute('SELECT * FROM {tn} WHERE {cn} = {d}'.\
                 format(tn = table_name, cn = col_name_0, d = os_data_request['items'][0]['date'])
    
conn.close()





c.execute('SELECT * FROM {tn} WHERE {cn} = {d}'.\
        format(tn = table_name, cn = column_name, d = day))

all_rows = c.fetchall()

"""