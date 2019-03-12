# Importing libraries
import sqlite3
import pandas as pd
from opensensors import Opensensors
from outlier_analytics import Outliers
from general_analytics import General
from heatmap_analytics import Heatmap
from data_preprocessing import preprocess

# pulling data and creating database
table_name = 'os_reading_'
# 'AUB', 'Reception', 'Meeting', '4thFloor'
# AUB first date: 2018-02-02
# Reception first dat: 2018-02-27
# Meeting Room first date: 2018-02-27

# Env Data first date: 2018-02-01

project = 'AUB'

osdp = Opensensors('2018-02-27', '2018-05-05', table_name + project, project)
data = osdp.data

# SQLite database to pandas dataframe
conn = sqlite3.connect(table_name + project + ".sqlite")
data = preprocess(pd.read_sql_query("SELECT * FROM " + project, conn))
conn.close()

#heat = data.iloc[:, 5:]
out = Outliers(data)
out.plot(5)

g = General(data)
g.plot_comparison_bars()

g.period_plot('month', 'circulation')
g.period_plot('month', 'exhibition')
g.period_plot('month', 'ai')
g.period_plot('month', 'code')
g.period_plot('month', 'vr')

g.period_plot('week', 'circulation')
g.period_plot('week', 'exhibition')
g.period_plot('week', 'ai')
g.period_plot('week', 'code')
g.period_plot('week', 'vr')

g.period_plot('day', 'circulation')
g.period_plot('day', 'exhibition')
g.period_plot('day', 'ai')
g.period_plot('day', 'code')
g.period_plot('day', 'vr')

ha = Heatmap(data)
ha.plot_average_heatmap()

ha.plot_heatmap_range(0, 200)
ha.plot_heatmap_stime(10, 670, 14)



from datetime import datetime, timedelta

from_date = datetime.strptime('2018-02-27', "%Y-%m-%d")
to_date = datetime.strptime('2018-05-05', "%Y-%m-%d")

sd = from_date
ed = to_date + timedelta(days = 1)

import requests

url_JWT = 'https://auth.opensensors.com/auth/login'
headers_JWT = { 'x-api-key': 'UoheJ3fp0w7CJisPi26NzNOw2rEPyMj67ovksMo1' }
API_access_token = requests.get(url_JWT, headers = headers_JWT, timeout = 1000).json()
# pulling data from opensensors api
url_GPM = 'https://api.opensensors.com/getProjectMessages';
headers_GPM = { 'Authorization': API_access_token.get('jwtToken') }

deviceId = ""
parameters = {'fromDate': sd.strftime('%Y-%m-%d'),
              'toDate': ed.strftime('%Y-%m-%d'),
              'projectUri': 'zaha-hadid',
              'deviceId': deviceId,
              'size': '500',
              'type': '',
              'cursor': ''}
data = requests.get(url_GPM, headers = headers_GPM, params = parameters).json()['items']