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
parameters = {'fromDate': '2018-02-04',
           'toDate': '2018-02-05',
           'projectUri': 'zaha-hadid',
           'size': '500',
           'type': 'modcamHeatmap',
           'cursor': ''}

os_data_request = requests.get(url_GPM, headers = headers_GPM, params = parameters).json()

##############################################################################
# CREATE DATABASE CONNECTION

conn = sqlite3.connect("os_reading_AUB_01.sqlite")
c = conn.cursor()
table_name = '\'' + str(os_data_request["nextCursor"]) + '\''
data = os_data_request['items'][0]
heatmap_len = len(data['heatmap'])
x_len = data['heatmap'][0]
y_len = data['heatmap'][1]

##############################################################################
# CREATE DATABASE + TABLE

heatmap_values = [''] * (heatmap_len - 2)
for i in range(0, heatmap_len - 2):
    heatmap_values[i] = '\'' + str(i) + '\'' + ' INTEGER'

heatmap_values = str(heatmap_values)
heatmap_values = heatmap_values[1:-1]
heatmap_values = heatmap_values.replace('\"', '')

sql_create_table = """ CREATE TABLE IF NOT EXISTS """ + table_name + """ (
                                        date INTEGER UNIQUE,
                                        tags TEXT,
                                        x_res INTEGER,
                                        y_res INTEGER,
                                        """ + str(heatmap_values) + """); """

c.execute(sql_create_table)

##############################################################################
# INSERT DATA

heatmap_column_names = []
for v in range(0, len(data['heatmap']) - 2):
    heatmap_column_names.append(str(v))

sql_replace_or_insert = """INSERT OR IGNORE INTO """ + table_name + """ (
                                        date,
                                        tags,
                                        x_res,
                                        y_res,
                                        """ + str(heatmap_column_names)[1:-1] + """)
                                        VALUES (
                                        """ + str(data['date']) + """,
                                        """ + '\'' + str(data['tags'][1]) + '\'' + """,
                                        """ + str(data['heatmap'][0]) + """,
                                        """ + str(data['heatmap'][1]) + """,
                                        """ + str(data['heatmap'][2:])[1:-1] + """); """

c.execute(sql_replace_or_insert)
conn.commit()
conn.close()