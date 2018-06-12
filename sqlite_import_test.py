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
# 'AUB', 'Reception', 'Meeting'
# AUB first date: 2018-02-02
# Reception first dat: 2018-02-27
# Meeting Room first date: 2018-02-27

project = 'Reception'

# osdp = Opensensors('2018-02-27', '2018-05-05', table_name + project, project)
# data = osdp.data

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