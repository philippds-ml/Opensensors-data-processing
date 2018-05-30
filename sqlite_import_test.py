# Importing libraries
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
from opensensors import Opensensors

# pulling data and creating database
table_name = 'os_reading_AUB'
osdp = Opensensors('2018-02-02', '2018-05-30', table_name)

# SQLite database to pandas dataframe
conn = sqlite3.connect("os_reading_AUB.sqlite")
data = pd.read_sql_query("SELECT * FROM " + table_name, conn)
heat = data.iloc[:, 5:]

row_count = len(data)
heatmap_length = len(heat.columns)