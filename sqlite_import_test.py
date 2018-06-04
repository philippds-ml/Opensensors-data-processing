# Importing libraries
import sqlite3
import pandas as pd
from opensensors import Opensensors
from outlier_analytics import Outliers
from general_analytics import General
from heatmap_analytics import Heatmap

# pulling data and creating database
table_name = 'os_reading_'
# 'AUB', 'Reception', 'Meeting'
# AUB first date: 2018-02-02
# Reception first dat:
# Meeting Room first date:

project = 'Reception'
osdp = Opensensors('2018-03-02', '2018-04-03', table_name + project, project)
data = osdp.data

def preprocess(data):
    data_dictionary = {}
    data2 = []
    heatmap_series = data.iloc[:,6:7]
    row_count = data.shape[0]
    for i in range(0, row_count):            
        temp = heatmap_series.iat[i, 0].split(',')
        heatmap_list = []
        for j in range(0, len(temp)):
            heatmap_list.append(int(temp[j]))                    
        data2.append(heatmap_list)

    for i in range(0, len(data2)):
        data_dictionary[i] =  data2[i]
    
    data2 = pd.DataFrame(data = data_dictionary).T

    
    data = pd.concat([data, data2], axis = 1)
    data = data.drop(columns='heatmap')
    return data

# SQLite database to pandas dataframe
conn = sqlite3.connect(table_name + project + ".sqlite")
data = preprocess(pd.read_sql_query("SELECT * FROM " + project, conn))
conn.close()

#heat = data.iloc[:, 5:]

out = Outliers(data)
out.plot(50)

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
ha.calc_average_heatmap()
ha.plot_average_heatmap()
ha.plot_heatmap_range(10, 20)

