import requests
import time
import sqlite3
from datetime import datetime, timedelta
import math

class Opensensors(object):
    
    def __init__(self, from_date, to_date, data_base_name):
        self.from_date = datetime.strptime(from_date, "%Y-%m-%d")
        self.to_date = datetime.strptime(to_date, "%Y-%m-%d")
        self.data_base_name = data_base_name + ".sqlite"
        
        self.compute()
    
    def compute(self):
        
        total_day_number = self.to_date - self.from_date
        start_date = self.from_date
        
        x_res = -1
        y_res = -1        
        heatmap_length = -1
        valid_data_item = -1
        
        # find valid item
        for k in range(0, total_day_number.days):
            check = False
            
            sd = start_date
            ed = start_date + timedelta(days = 1)            
            try:
                data = self.pull_data(sd.strftime('%Y-%m-%d'), ed.strftime('%Y-%m-%d'))
                if(len(data) > 0):    
                    for o in range(0, len(data)):
                        if(len(data[o]['heatmap']) > 0):
                            x_res = data[o]['heatmap'][0]
                            y_res = data[o]['heatmap'][1]
                            heatmap_length = len(data[o]['heatmap'])
                            valid_data_item = data[o]
                            
                            print("x resolution", x_res)
                            print("y resolution", y_res)
                            print("heatmap size", heatmap_length)
                            
                            check = True
                            break
            except:
                check = False
            
            if(check):
                break
        
        # creating database
        self.creating_db(valid_data_item)        
        
        # fill DB with dummy values
        heat_list = []
        heat_list.append(x_res)
        heat_list.append(y_res)
        heat_list += [0] * (heatmap_length - 2)
        
        dummy_values = [{}] *  total_day_number.days * 24
        
        print("total hour count", total_day_number.days * 24)
        
        for i in range(0, total_day_number.days * 24):  
            human_time = self.from_date + timedelta(hours = 1 * i)
            print("human time:", human_time)
            dummy_values[i] = {'human_time': str(human_time)}
            
            epoch_time = int(time.mktime(human_time.timetuple()))                          
            dummy_values[i].update({'date': epoch_time})
            
            dummy_values[i].update({'heatmap': heat_list})
            dummy_values[i].update({'dayOfTheWeek': human_time.today().weekday()})
            dummy_values[i].update({'deviceId': valid_data_item['deviceId']})
            dummy_values[i].update({'type': valid_data_item['type']})
            dummy_values[i].update({'tags': valid_data_item['tags']})
        
        self.insert_data_into_db(dummy_values)
        
        """
        # fill DB with Sensor Readings
        package_count = math.ceil(total_day_number.days / 20)
        
        for j in range(0, package_count):
            
            if(package_count > 1 and j > 0):
                start_date = end_date
                end_date = end_date + timedelta(days = 20)
                if(self.to_date < end_date):
                    end_date = self.to_date
            elif(package_count > 1 and j == 0):
                end_date = start_date + timedelta(days = 20)
            
            print("package start:", start_date, " end:", end_date)
            
            #d = self.preprocess_data(self.pull_data(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
            #self.local_data += d
        """
        
                    
    
    ##############################################################################
    # OS METHODS    
    # pull JWT
    
    def pull_data(self, from_d, to_d):
        
        print(from_d, " ", to_d)
        
        url_JWT = 'https://auth.opensensors.com/auth/login'
        headers_JWT = { 'x-api-key': 'UoheJ3fp0w7CJisPi26NzNOw2rEPyMj67ovksMo1' }
        API_access_token = requests.get(url_JWT, headers = headers_JWT, timeout = 1000).json()
        # pulling data from opensensors api
        url_GPM = 'https://api.opensensors.com/getProjectMessages';
        headers_GPM = { 'Authorization': API_access_token.get('jwtToken') }
        
        # 'fromDate': '2018-02-02'
        # 'toDate': '2018-02-20'
        
        parameters = {'fromDate': from_d,
                      'toDate': to_d,
                      'projectUri': 'zaha-hadid',
                      'deviceId': '5a5609dc1ac137000520d91f',
                      'size': '500',
                      'type': 'modcamHeatmap',
                      'cursor': ''}
        data = requests.get(url_GPM, headers = headers_GPM, params = parameters).json()['items']
        
        return data
    
    # pre process data
    def preprocess_data(self, d):
        
        data = d
        print("CHECKING DATA PULL --------")  
        print("data size:", len(data))
        
        # define duration of sequence
        data_0 = data[0]['date']
        first_time = datetime.fromtimestamp(data_0 // 1000)
        first_time = first_time.replace(hour = 0, minute = 0, second = 0)
        
        print("First time", str(first_time))
        
        data_last = data[len(data) - 1]['date']
        last_time = datetime.fromtimestamp(data_last // 1000)
        print("Last time", str(last_time))
        last_time = last_time.replace(hour = 0, minute = 0, second = 0)
        
        
        #print(data[len(data) - 1]['date'])
        
        
        main_difference = (last_time - first_time).days
        # print("difference:", main_difference)
        data_full = [{}] * (main_difference + 1) * 24
        
        print("data_full size:", len(data_full))
        
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

    def creating_db(self, data_item):
        
        ##############################################################################
        # OPENING DATA BASE FILE
        conn = sqlite3.connect(self.data_base_name)
        c = conn.cursor()
        table_name = 'OS_READING_AUB'
        
        ##############################################################################
        # CREATING NEW DATABASE
        
        heatmap_length = len(data_item['heatmap'])
        
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
        conn.close()
        
    def insert_data_into_db(self, d):
        
        ##############################################################################
        # INSERT DATA
        conn = sqlite3.connect(self.data_base_name)
        c = conn.cursor()
        table_name = 'OS_READING_AUB'
        
        heatmap_column_names = []        
        for v in range(0, len(d[0]['heatmap']) - 2):
            heatmap_column_names.append(str(v))
        
        for p in range(0, len(d)):
            sql_replace_or_insert = """INSERT OR IGNORE INTO """ + table_name + """ (
                                                date,
                                                human_time,
                                                tags,
                                                x_res,
                                                y_res,
                                                """ + str(heatmap_column_names)[1:-1] + """)
                                                VALUES (
                                                """ + str(d[p]['date']) + """,
                                                """ + '\'' + str(d[p]['human_time']) + '\'' + """,
                                                """ + '\'' + str(d[p]['tags'][1]) + '\'' + """,
                                                """ + str(d[p]['heatmap'][0]) + """,
                                                """ + str(d[p]['heatmap'][1]) + """,
                                                """ + str(d[p]['heatmap'][2:])[1:-1] + """);"""
        
            c.execute(sql_replace_or_insert)
            conn.commit()
        
        
        conn.close()
    
    def get_all_data(self):
        # GET ALL DATA FROM DATABASE        
        conn = sqlite3.connect(self.data_base_name)
        c = conn.cursor()
        table_name = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in table_name:
            table_name = name[0]
        
        
        dataCopy = c.execute("select count(*) from """ + table_name)
        row_count = dataCopy.fetchone()
        row_count = row_count[0]
        
        c.execute('SELECT * FROM {tn}'.\
                      format(tn = table_name))
        return c.fetchall()

