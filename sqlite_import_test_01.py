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

# create table in database
# creating sqlite task
table_name = '\'' + str(os_data_request["nextCursor"]) + '\''

data = os_data_request['items'][0]
heatmap_len = len(data['heatmap'])
x_len = data['heatmap'][0]
y_len = data['heatmap'][1]

heatmap_values = [''] * (heatmap_len - 2)
for i in range(0, heatmap_len - 2):
    heatmap_values[i] = '\'' + str(i) + '\'' + ' INTEGER'

heatmap_values = str(heatmap_values)
heatmap_values = heatmap_values[1:-1]
heatmap_values = heatmap_values.replace('\"', '')

sql_create_projects_table_01 = """ CREATE TABLE IF NOT EXISTS """ + table_name + """ (
                                        date INTEGER,
                                        tags TEXT,
                                        x_res INTEGER,
                                        y_res INTEGER,
                                        """ + str(heatmap_values) + """); """


# create a database connection
conn = sqlite3.connect("os_reading_AUB_01.sqlite")
c = conn.cursor()
c.execute(sql_create_projects_table_01)

heatmap_values = heatmap_values.replace('\'', '')
heatmap_values = heatmap_values.replace('INTEGER', '')

x = 0
y = 0

for v in range (2, heatmap_len):
    
    sql_repace_or_insert = """INSERT OR REPLACE INTO """ + table_name + """ (date, tags, x_res, y_res, """ + heatmap_values + """) 
                                        VALUES (""" + str(data['date']) + """,
                                                """ + str(data['tags'][1]) + """,
                                                """ + str(data['date']) + """,
                                                COALESCE((SELECT heatmap FROM """ + table_name + """ WHERE x = """ + str(x) + """ AND y = """ + str(y) + """ AND date = """ + str(data['date']) + """), """ + str(data['heatmap'][v]) + """),
                                                
                                                """ + data['type'] + """
                                                ); """
    
    if(x == x_len):
        x = 0
        y += 1
        print(y)
    
    # sql_insert = """ INSERT INTO """ + table_name + """(date, dayOfTheWeek, deviceId, heartbeat, x, y, heatmap, tags, types) VALUES(?,?,?,?,?,?,?,?,?) """
    task_1 = (data['date'], data['dayOfTheWeek'], data['deviceId'], str(data['heartbeat']), x, y, data['heatmap'][v], data['tags'][1], data['type'])

    #c.execute(sql_repace_or_insert, task_1)
    c.execute(sql_repace_or_insert)
    
    x += 1

conn.commit()
conn.close()
