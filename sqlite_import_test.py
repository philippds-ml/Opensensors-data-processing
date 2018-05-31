# Importing libraries
import sqlite3
import pandas as pd
from opensensors import Opensensors
from outlier_analytics import Outliers
from general_analytics import General

# pulling data and creating database
table_name = 'os_reading_AUB'
osdp = Opensensors('2018-02-02', '2018-05-30', table_name)

# SQLite database to pandas dataframe
conn = sqlite3.connect("os_reading_AUB.sqlite")
data = pd.read_sql_query("SELECT * FROM " + table_name, conn)
heat = data.iloc[:, 5:]

out = Outliers(data)
out.plot(1)

g = General(data)
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