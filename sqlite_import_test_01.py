# Importing libraries
import sqlite3
import requests
import time
import numpy as np
import matplotlib.pyplot as plt
import math

##############################################################################
# OS PULL

# pull JWT
url_JWT = 'https://auth.opensensors.com/auth/login'
headers_JWT = { 'x-api-key': 'UoheJ3fp0w7CJisPi26NzNOw2rEPyMj67ovksMo1' }
API_access_token = requests.get(url_JWT, headers = headers_JWT, timeout = 1000).json()

# pulling data from opensensors api
url_GPM = 'https://api.opensensors.com/getProjectMessages';
headers_GPM = { 'Authorization': API_access_token.get('jwtToken') }
parameters = {'fromDate': '2018-05-01',
           'toDate': '2018-05-18',
           'projectUri': 'zaha-hadid',
           'deviceId': '5a5609dc1ac137000520d91f',
           'size': '500',
           'type': 'modcamHeatmap',
           'cursor': ''}

os_data_request = requests.get(url_GPM, headers = headers_GPM, params = parameters).json()

##############################################################################
# PREPROCESS DATA

data = os_data_request['items']

x_len = 0
y_len = 0
empty_data_replacement = []

item_number = len(data)

for j in range(0, item_number):
    if not(len(data[j]['heatmap']) == 0):
        print(len(data[j]['heatmap']))
        x_len = data[j]['heatmap'][0]
        y_len = data[j]['heatmap'][1]
        empty_data_replacement.append(x_len)
        empty_data_replacement.append(y_len)
        empty_data_replacement += [0] * (len(data[j]['heatmap']) - 2)
        break

for k in range(0, item_number):
    if (len(data[k]['heatmap']) == 0):
        data[k]['heatmap'] = empty_data_replacement

heatmap_length = len(data[0]['heatmap'])

##############################################################################
# OPENING DATA BASE FILE

conn = sqlite3.connect("os_reading_AUB_03.sqlite")
c = conn.cursor()
table_name = 'OS_READING_AUB'

##############################################################################
# CREATING NEW DATABASE
heatmap_values = [''] * (heatmap_length - 2)

for i in range(0, heatmap_length - 2):
    heatmap_values[i] = '\'' + str(i) + '\'' + ' INTEGER'

heatmap_values = str(heatmap_values)
heatmap_values = heatmap_values[1:-1]
heatmap_values = heatmap_values.replace('\"', '')


sql_create_table = """ CREATE TABLE IF NOT EXISTS """ + table_name + """ (
                                        date INTEGER UNIQUE,
                                        human_time TEXT,
                                        tags TEXT,
                                        x_res INTEGER,
                                        y_res INTEGER,
                                        """ + str(heatmap_values) + """); """

c.execute(sql_create_table)

##############################################################################
# INSERT DATA

conn = sqlite3.connect("os_reading_AUB_03.sqlite")
c = conn.cursor()

heatmap_column_names = []
for v in range(0, heatmap_length - 2):
    heatmap_column_names.append(str(v))

for p in range(0, item_number):
    sql_replace_or_insert = """INSERT OR IGNORE INTO """ + table_name + """ (
                                        date,
                                        human_time,
                                        tags,
                                        x_res,
                                        y_res,
                                        """ + str(heatmap_column_names)[1:-1] + """)
                                        VALUES (
                                        """ + str(data[p]['date']) + """,
                                        """ + '\'' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data[p]['date']) / 1000))) + '\'' + """,
                                        """ + '\'' + str(data[p]['tags'][1]) + '\'' + """,
                                        """ + str(data[p]['heatmap'][0]) + """,
                                        """ + str(data[p]['heatmap'][1]) + """,
                                        """ + str(data[p]['heatmap'][2:])[1:-1] + """); """

    c.execute(sql_replace_or_insert)
    conn.commit()


conn.close() 

##############################################################################
# INSERT DATA

conn = sqlite3.connect("os_reading_AUB_03.sqlite")
c = conn.cursor()

dataCopy = c.execute("select count(*) from """ + table_name)
row_count = dataCopy.fetchone()
row_count = row_count[0]

c.execute('SELECT * FROM {tn}'.\
              format(tn = table_name))
all_rows = c.fetchall()






outlier_sum = []

for r in range(5, heatmap_length - 2 + 5):    
    # sort list
    sorted_list = []
    for g in range(0, row_count):
        sorted_list.append(all_rows[g][r])
    sorted(sorted_list)
    
    # find lower and upper quartile and IQR
    x_025 = sorted_list[math.floor(row_count * 0.25 + 1) - 1]
    x_075 = sorted_list[math.floor(row_count * 0.75 + 1) - 1]
    
    iqr = x_075 - x_025
    
    # 
    temp_outlier_sum = 0
    for m in range(5, heatmap_length - 2 + 5):
        if all_rows[r][m] > iqr * 1.5:
            temp_outlier_sum += 1
    outlier_sum.append(temp_outlier_sum)



ave = []
for r in range(5, heatmap_length - 2 + 5):    
    value_sum = 0
    for g in range(0, row_count): 
        value_sum += int(all_rows[g][r])
    ave.append(value_sum / row_count)


for b in range(0, row_count):    
    temp_outlier_sum = 0
    for m in range(5, heatmap_length - 2 + 5):
        if (math.sqrt(math.pow(ave[m - 5] - all_rows[b][m], 2)) > (ave[m - 5] * 1.5)):
            temp_outlier_sum += 1
    outlier_sum.append(temp_outlier_sum)

# Visualising the Training set results
arrs = []
temp_arr = []
for m in range(5, heatmap_length - 2):
    
    if (m - 5) != 0 and (m - 5) % 38 == 0:
        temp_arr = np.array(temp_arr)
        arrs.append(temp_arr)
        temp_arr = []
        temp_arr.append(int(all_rows[14][m]))
    else:
        temp_arr.append(int(all_rows[14][m]))

aaa = np.array(arrs)

plt.imshow(aaa, cmap='hot', interpolation='nearest')
plt.show()

# Visualising averages
X = []
for n in range(1, heatmap_length - 1):
    X.append(n)

plt.scatter(X, ave, color = 'red')
plt.title('Visualizing Average Values')
plt.xlabel('index')
plt.ylabel('averege count')
plt.show()












