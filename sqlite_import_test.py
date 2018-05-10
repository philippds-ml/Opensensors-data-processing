import sqlite3
import pandas as pd
import requests
from requests_oauthlib import OAuth1

conn = sqlite3.connect('AUBsmall.sqlite')

dataset = pd.read_sql_query('select * from Observations;', conn)

conn.close()

# pull JWT

url_JWT = 'https://auth.opensensors.com/auth/login'
auth = OAuth1('QYi7JGgICN2wKLP0K1cof8v6veepaSu97R31G0m7')
requests.get(url_JWT, auth = auth)


# pulling data from opensensors api


url_GPM = 'https://api.opensensors.com/getProjectMessages';
payload = {'fromDate': '2018-02-02',
           'toDate': '2018-02-03',
           'projectUri': 'zaha-hadid',
           'size': '500',
           'type': 'modcamHeatmap',
           'cursor': ''}

r = requests.get(url_GPM, params=payload)




"""
table_name = 'Observations'
column_name = 'id'
day = 0

c.execute('SELECT * FROM {tn} WHERE {cn} = {d}'.\
        format(tn = table_name, cn = column_name, d = day))

all_rows = c.fetchall()
"""



