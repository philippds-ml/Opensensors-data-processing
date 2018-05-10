import sqlite3
import pandas as pd
import requests

# connect to database
conn = sqlite3.connect('AUBsmall.sqlite')
dataset = pd.read_sql_query('select * from Observations;', conn)
conn.close()

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
heatmaps = os_data_request['items'][0]['heatmap']

# import json
# decoded = json.loads(os_data_request.encoding)

"""
table_name = 'Observations'
column_name = 'id'
day = 0

c.execute('SELECT * FROM {tn} WHERE {cn} = {d}'.\
        format(tn = table_name, cn = column_name, d = day))

all_rows = c.fetchall()
"""