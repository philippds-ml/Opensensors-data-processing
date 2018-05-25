# Importing libraries
import sqlite3
import requests
import time
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

##############################################################################
# OS PULL

# pull JWT
def pull_data():        
    url_JWT = 'https://auth.opensensors.com/auth/login'
    headers_JWT = { 'x-api-key': 'UoheJ3fp0w7CJisPi26NzNOw2rEPyMj67ovksMo1' }
    API_access_token = requests.get(url_JWT, headers = headers_JWT, timeout = 1000).json()
    # pulling data from opensensors api
    url_GPM = 'https://api.opensensors.com/getProjectMessages';
    headers_GPM = { 'Authorization': API_access_token.get('jwtToken') }
    parameters = {'fromDate': '2018-02-27',
                  'toDate': '2018-02-29',
                  'projectUri': 'zaha-hadid',
                  'deviceId': '5a5609dc1ac137000520d91f',
                  'size': '500',
                  'type': 'modcamHeatmap',
                  'cursor': ''}
    data = requests.get(url_GPM, headers = headers_GPM, params = parameters).json()['items']
    
    print("CHECKING DATA PULL --------")
    print(len(data))
    
    return data

# pre process data
def preprocess_data(d):
    
    data = d
    
    # define duration of sequence
    from datetime import datetime, timedelta

    data_0 = data[0]['date']
    first_time = datetime.fromtimestamp(data_0 // 1000)
    first_time = first_time.replace(hour = 0, minute = 0, second = 0)
    
    data_last = data[len(data) - 1]['date']
    last_time = datetime.fromtimestamp(data_last // 1000)
    last_time = last_time.replace(hour = 0, minute = 0, second = 0)
    
    main_difference = (last_time - first_time).days
    
    data_full = [{}] * (main_difference * 2) * 24
    
    valid_item = {}
    valid_item_index = -1

    for i in range(0, len(data)):
        current_time = datetime.fromtimestamp(data[i]['date'] // 1000)
        difference = current_time - first_time
        index = (difference.seconds // 3600) + 24 * difference.days
        data_full[index] = data[i]
        if not('date' in valid_item):
            valid_item = data[i]
            valid_item_index = index

    missing_indexes = []
    for j in range(0, len(data_full)):
        if not('date' in data_full[j]):
            missing_indexes.append(j)
            
    heat_list = []
    heat_list.append(valid_item['heatmap'][0])
    heat_list.append(valid_item['heatmap'][1])
    heat_list += [0] * (len(valid_item['heatmap']) - 2)
    
    for g in missing_indexes:
        data_full[g] = {'date': valid_item['date'] + (g - valid_item_index) * 3600000}
        data_full[g].update({'heatmap': heat_list})
    
        item_time = datetime.fromtimestamp(data_full[g]['date'] //1000).day
        valid_item_time = datetime.fromtimestamp(valid_item['date'] //1000).day
        
        if(item_time == valid_item_time):
            data_full[g].update({'dayOfTheWeek': valid_item['dayOfTheWeek']})
        else:
            data_full[g].update({'dayOfTheWeek': (datetime.fromtimestamp(data_full[g]['date'] //1000)).today().weekday()})
    
        data_full[g].update({'deviceId': valid_item['deviceId']})
        data_full[g].update({'heartbeat': valid_item['heartbeat']})
        data_full[g].update({'tags': valid_item['tags']})
        data_full[g].update({'type': valid_item['type']})
    

    for h in data:
        if(len(h['heatmap']) == 0):
            h.update({'heatmap': heat_list}) 

    
    return data_full


pull = preprocess_data(pull_data())

##############################################################################
# OPENING DATA BASE FILE

conn = sqlite3.connect("os_reading_AUB_05.sqlite")
c = conn.cursor()
table_name = 'OS_READING_AUB'

##############################################################################
# CREATING NEW DATABASE

heatmap_length = len(pull[0]['heatmap'])

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
                                        """ + str(heatmap_values) + """);"""

c.execute(sql_create_table)

##############################################################################
# INSERT DATA

conn = sqlite3.connect("os_reading_AUB_05.sqlite")
c = conn.cursor()

heatmap_column_names = []
for v in range(0, heatmap_length - 2):
    heatmap_column_names.append(str(v))

for p in range(0, len(pull)):
    sql_replace_or_insert = """INSERT OR IGNORE INTO """ + table_name + """ (
                                        date,
                                        human_time,
                                        tags,
                                        x_res,
                                        y_res,
                                        """ + str(heatmap_column_names)[1:-1] + """)
                                        VALUES (
                                        """ + str(pull[p]['date']) + """,
                                        """ + '\'' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(pull[p]['date']) / 1000))) + '\'' + """,
                                        """ + '\'' + str(pull[p]['tags'][1]) + '\'' + """,
                                        """ + str(pull[p]['heatmap'][0]) + """,
                                        """ + str(pull[p]['heatmap'][1]) + """,
                                        """ + str(pull[p]['heatmap'][2:])[1:-1] + """);"""

    c.execute(sql_replace_or_insert)
    conn.commit()


conn.close()

##############################################################################
# GET ALL DATA FROM DATABASE

conn = sqlite3.connect("os_reading_AUB_03.sqlite")
c = conn.cursor()
table_name = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
for name in table_name:
    table_name = name[0]


dataCopy = c.execute("select count(*) from """ + table_name)
row_count = dataCopy.fetchone()
row_count = row_count[0]

c.execute('SELECT * FROM {tn}'.\
              format(tn = table_name))
all_rows = c.fetchall()





# CALCULATE OUTLIERS
outlier_pixel_sum = []
outlier_flag = [0] * row_count

for r in range(5, len(all_rows[0])):    
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
    for m in range(0, row_count):
        if all_rows[m][r] > iqr * 1.5:
            temp_outlier_sum += 1
            outlier_flag[m] += 1
            
    outlier_pixel_sum.append(temp_outlier_sum)
    
    
outlier_flag_sorted = sorted(outlier_flag)
x_025 = outlier_flag_sorted[math.floor(row_count * 0.25 + 1) - 1]
x_075 = outlier_flag_sorted[math.floor(row_count * 0.75 + 1) - 1]
    
iqr = x_075 - x_025

outlier_index = []

for a in range(0, row_count):
    if outlier_flag[a] > iqr * 1.5:
        outlier_index.append(a)

def plot_heatmaps(indexes, count, col):
    #plt.title(all_rows[][])    
    # number_of_heatmaps = len(indexes)
    arrs = []
    temp_arr = []
    
    for g in range(0, count):
        
        index_x = 0
        for m in range(5, len(all_rows[0])):
            if index_x == 38:
                temp_arr.append(all_rows[indexes[g]][m])
                arrs.append(np.array(temp_arr))
                temp_arr = []
                index_x = 0
                
            else:
                temp_arr.append(all_rows[indexes[g]][m])
                index_x += 1
        
        heatmap_0 = np.array(arrs)
        
        plt.subplot(math.ceil(count / col), col, g + 1)
        plt.imshow(heatmap_0, cmap='hot', interpolation='gaussian')
 
        title = all_rows[indexes[g]][1] + " | " + str(outlier_flag[indexes[g]])
    
        plt.title(title, loc = 'left', fontsize = 7)
        arrs = []
        temp_arr = []
        
        for i in range(0, 897):
            if(i < 8):
                plt.scatter(i, 0, color = 'blue', s = 1)
            if((i >= 39 and i % 39 < 8) and (int(i / 39) < 12)):
                plt.scatter(i % 39, int(i / 39), color = 'blue', s = 10)
            
            if(int(i / 39) >= 18 and i % 39 > 10 and i % 39 <= 25 and (int(i / 39) < 21 or i % 39 > 14 or i % 39 < 12)):
                plt.scatter(i % 39, int(i / 39), color = 'red', s = 10)
                
            
            if(int(i / 39) >= 10 and i % 39 > 25):
                plt.scatter(i % 39, int(i / 39), color = 'green', s = 10)
        
        plt.scatter(7, 4, color = 'cyan', s = 30)
        plt.scatter(7, 14, color = 'cyan', s = 30)
        plt.scatter(18, 11, color = 'cyan', s = 30)
        

    plt.show()

outlier_index_cropped = []

for i in outlier_index:
    if(int(outlier_flag[i]) > 400):
        outlier_index_cropped.append(i)


plot_heatmaps(outlier_index_cropped, 1, 1)


# SQLite database to pandas dataframe
conn = sqlite3.connect("os_reading_AUB_03.sqlite")
df = pd.read_sql_query("SELECT * FROM " + table_name, conn)

X = df.iloc[:, :].values # -1 means all the columns except the last one
y = df.iloc[:, 1].values # dependend variable


df = df.iloc[:, 5:]

count_ai = 0
count_code = 0
count_vr = 0
count_circulation = 0


ai_time = [0] * 24
code_time = [0] * 24
vr_time = [0] * 24

circulation_time = [0] * 24
exhibition_time = [0] * 24

X = [0] * 24

time_index = 0
global_index = 0

for row in df.iterrows():
    
    print(str(time_index) + " - " + str(all_rows[global_index][1]))
    global_index += 1
    
    
    time_temp = 0
    exhibition_temp = 0
    
    ai_temp = 0
    code_temp = 0
    vr_temp = 0
    
    for i in range(0, 897):
        if(i < 8):
            count_ai += row[1][i]
            exhibition_temp += row[1][i]
            ai_temp += row[1][i]
        elif((i >= 39 and i % 39 < 8) and (int(i / 39) < 12)):
            count_ai += row[1][i]
            exhibition_temp += row[1][i] 
            ai_temp += row[1][i]  
        elif(int(i / 39) >= 18 and i % 39 > 10 and i % 39 <= 25 and (int(i / 39) < 21 or i % 39 > 14 or i % 39 < 12)):
            count_code += row[1][i]
            exhibition_temp += row[1][i]
            code_temp += row[1][i]  
        elif(int(i / 39) >= 10 and i % 39 > 25):
            count_vr += row[1][i]
            exhibition_temp += row[1][i]
            vr_temp += row[1][i]  
        else:
            count_circulation += row[1][i]
            time_temp += row[1][i]
    
    circulation_time[time_index] += time_temp
    exhibition_time[time_index] += exhibition_temp
    ai_time[time_index] += ai_temp
    code_time[time_index] += code_temp
    vr_time[time_index] += vr_temp    
    
    if(time_index < 23):
        time_index += 1
    else:
        time_index = 0
    
    if(global_index == 960):    
        break

count_total = count_ai + count_code + count_vr + count_circulation

for t in range(0, len(circulation_time)):
    X[t] = t
    circulation_time[t] /= (count_total / 100)
for t in range(0, len(circulation_time)):
    exhibition_time[t] /= (count_total / 100)
    ai_time[t] /= (count_total / 100)
    code_time[t] /= (count_total / 100)
    vr_time[t] /= (count_total / 100)

count_total /= 100
count_ai /= count_total
count_code /= count_total
count_vr /= count_total
count_circulation /= count_total

plt.xlabel('Hour')
plt.ylabel('Percentage (%)')
plt.plot(X, circulation_time, color = 'red', lw = 2, label = 'circulation usage')
plt.plot(X, exhibition_time, color = 'blue', lw = 2, label = 'exhibition visit')
plt.legend()
plt.show()

plt.xlabel('Hour')
plt.ylabel('Percentage (%)')
plt.plot(X, ai_time, color = 'red', lw = 2, label = 'ai exhibition visit')
plt.plot(X, code_time, color = 'blue', lw = 2, label = 'code exhibition visit')
plt.plot(X, vr_time, color = 'green', lw = 2, label = 'vr exhibition visit')
plt.legend()
plt.show()

plt.ylabel('Percentage (%)')
plt.bar([0, 1, 2], [(count_ai / (count_ai + count_code + count_vr)) * 100, (count_code / (count_ai + count_code + count_vr)) * 100, (count_vr / (count_ai + count_code + count_vr)) * 100], color = ['red', 'blue', 'green'])
plt.xticks([0, 1, 2], ("AI visits", "Code visits", "VR visits"))
plt.legen()
plt.show()











            
            
        

















# CALC GOBAL AVERAGE
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

# PLOT MULTIPLE HEATMAPS
def plot_heatmaps(number_of_heatmaps):
    #plt.title(all_rows[][])
    
    number_of_heatmaps = number_of_heatmaps * 24
    arrs = []
    temp_arr = []
    
    for g in range(number_of_heatmaps - 24, number_of_heatmaps):
        
        index_x = 0
        for m in range(5, heatmap_length + 5 - 2):
            if index_x == 38:
                temp_arr.append(int(all_rows[g][m]))
                arrs.append(np.array(temp_arr))
                temp_arr = []
                index_x = 0
                
            else:
                temp_arr.append(int(all_rows[g][m]))
                index_x += 1
        
        heatmap_0 = np.array(arrs)
        
        plt.subplot(4, 6, g - (number_of_heatmaps - 24) + 1)
        plt.imshow(heatmap_0, cmap='hot', interpolation='nearest')
 
        plt.title(all_rows[g][1], loc = 'left', fontsize = 10)
        arrs = []
        temp_arr = []
       

    plt.show()
    
    
plot_heatmaps(19)

number_of_heatmaps = len(all_rows)
arrs = []
temp_arr = []
aaa = []

for g in range(0, number_of_heatmaps):
    index_x = 0
    for m in range(5, heatmap_length + 5 - 2):
        if index_x == 38:
            temp_arr.append(int(all_rows[g][m]))
            arrs.append(np.array(temp_arr))
            temp_arr = []
            index_x = 0
        else:
            temp_arr.append(int(all_rows[g][m]))
            index_x += 1
    
    if g == 0:
        aaa = np.array(arrs)
    else:
        aaa += np.array(arrs)
    
    arrs = []
    temp_arr = []
    
heatmap_0 = aaa
plt.imshow(heatmap_0, interpolation='nearest')
plt.show()


arrs = []
temp_arr = []
index_x = 0

for s in range(0, heatmap_length - 2):
    if index_x == 38:
        temp_arr.append(outlier_sum[s])
        arrs.append(np.array(temp_arr))
        temp_arr = []
        index_x = 0
    else:
        temp_arr.append(outlier_sum[s])
        index_x += 1

heatmap_0 = np.array(arrs)
plt.imshow(heatmap_0, interpolation='nearest')
plt.show()
