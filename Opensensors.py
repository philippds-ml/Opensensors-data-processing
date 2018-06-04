import requests
import time
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

class Opensensors(object):
    
    def __init__(self, from_date, to_date, data_base_name, project):
        self.from_date = datetime.strptime(from_date, "%Y-%m-%d")
        self.to_date = datetime.strptime(to_date, "%Y-%m-%d")
        self.project = project
        self.data_base_name = data_base_name + ".sqlite"
        
        self.data = pd.DataFrame()
        self.date = []
        self.heatmap_length = -1
        self.x_res = -1
        self.y_res = -1
        self.deviceId = ""
        self.tags = ""               
        
        self.compute()
    
    def compute(self):
        print("pulling data from Opensensors...")
        total_day_number = self.to_date - self.from_date
        start_date = self.from_date
        end_date = self.to_date
                
        # FIND VALID ITEM
        for k in range(0, total_day_number.days):
            check = False            
            sd = start_date
            ed = start_date + timedelta(days = 1)
            try:
                data = self.pull_data(sd.strftime('%Y-%m-%d'), ed.strftime('%Y-%m-%d'))
                if(len(data) > 0):    
                    for o in range(0, len(data)):
                        if(len(data[o]['heatmap']) > 0):
                            self.x_res = data[o]['heatmap'][0]
                            self.y_res = data[o]['heatmap'][1]
                            self.heatmap_length = len(data[o]['heatmap']) - 2
                            self.deviceId = data[o]['deviceId']
                            self.tags = data[o]['tags'][1]
                            check = True
                            break
            except:
                check = False            
            if(check):
                break
        ###################

        # CREATING DATABASE
        self.creating_db()
        concatinated_data = []
        for j in range(0, total_day_number.days):
            if(j != 0):
                start_date = start_date + timedelta(days = 1)
                end_date = start_date + timedelta(days = 1)
            else:
                end_date = start_date + timedelta(days = 1)            

            d = self.pull_data(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            
            for m in range(0, len(d)):
                sd = start_date
                sd = sd + timedelta(hours = 1 * m)
                if(len(d[m]['heatmap']) != 0):
                    #print(len(d[m]['heatmap']))
                    d[m]['date'] = int(time.mktime(sd.timetuple()))                
                    d[m].update({'human_time': str(sd)})
                    
                    if(self.project == 'AUB'):
                        for i in range(0, len(d[m]['heatmap']) - 2):
                            if not((int(i / 39) < 21 or i % 39 > 15 or i % 39 < 12)):
                                d[m]['heatmap'][i + 2] = 0
                                #print("replace with 0 | y:", int(i / 39), " x:", i % 39)
                    
                    d[m].update({'x_res': self.x_res})
                    d[m].update({'y_res': self.y_res})
                    d[m].update({'tags': self.tags})
                                
                    heat_item = ""
                    for i in range(0, self.heatmap_length):
                        heat_item += str(d[m]['heatmap'][i + 2])
                        if i < self.heatmap_length - 1:
                            heat_item += ","
                    
                    d[m].update({'heatmap': heat_item})            
                    concatinated_data.append(d[m])
        
        ###################
        
        # fill DB with dummy values        
        dummy_heatmap_string = ""
        for i in range(0, self.heatmap_length):
            dummy_heatmap_string += str(0)
            if i < self.heatmap_length - 1:
                dummy_heatmap_string += ','
         
        dummy_values = [{}] *  total_day_number.days * 24        
        for i in range(0, total_day_number.days * 24):  
            human_time = self.from_date + timedelta(hours = 1 * i)            
            ht = human_time
            epoch_time = int(time.mktime(ht.timetuple()))                       
            dummy_values[i] = {'date': int(epoch_time)}
            dummy_values[i].update({'human_time': str(human_time)})
            dummy_values[i].update({'x_res': self.x_res})
            dummy_values[i].update({'y_res': self.y_res})
            
            dummy_values[i].update({'heatmap': dummy_heatmap_string})
            dayOfTheWeek = human_time.isoweekday()
            if(dayOfTheWeek == 7):
                dayOfTheWeek = 0
            dummy_values[i].update({'dayOfTheWeek': dayOfTheWeek})
            dummy_values[i].update({'deviceId': self.deviceId})
            dummy_values[i].update({'tags': self.tags})
                
        output_data = dummy_values        
        for c in range(0, total_day_number.days * 24):
            for b in range(0, len(concatinated_data)):
                if(dummy_values[c]['date'] == concatinated_data[b]['date']):
                    output_data[c] = concatinated_data[b]
                    output_data[c].update({'human_time': dummy_values[c]['human_time']})
                    break
        
        
        for i in range(0, len(output_data)):
            print(output_data[i]['tags'])
        
        self.insert_data_into_db(output_data)
        self.data = output_data
        #self.data = output_data[0]['heatmap']
        
        print("... Done!")
        
    
    ##############################################################################
    # OS METHODS
    
    def pull_data(self, from_d, to_d):        
        url_JWT = 'https://auth.opensensors.com/auth/login'
        headers_JWT = { 'x-api-key': 'UoheJ3fp0w7CJisPi26NzNOw2rEPyMj67ovksMo1' }
        API_access_token = requests.get(url_JWT, headers = headers_JWT, timeout = 1000).json()
        # pulling data from opensensors api
        url_GPM = 'https://api.opensensors.com/getProjectMessages';
        headers_GPM = { 'Authorization': API_access_token.get('jwtToken') }
        
        deviceId = ""
        
        if(self.project == 'AUB'): deviceId = '5a5609dc1ac137000520d91f'
        if(self.project == 'Reception'): deviceId = '5a5609981ac137000520d91c'
        if(self.project == 'Meeting'): deviceId = '5a7bfe2b3865840006b930b4'
        
        parameters = {'fromDate': from_d,
                      'toDate': to_d,
                      'projectUri': 'zaha-hadid',
                      'deviceId': deviceId,
                      'size': '500',
                      'type': 'modcamHeatmap',
                      'cursor': ''}
        data = requests.get(url_GPM, headers = headers_GPM, params = parameters).json()['items']        
        return data

    def creating_db(self):
        # OPENING DATA BASE FILE
        conn = sqlite3.connect(self.data_base_name)        
        c = conn.cursor()
        
        sql_create_table = 'CREATE TABLE IF NOT EXISTS ' + self.project + """ (date INTEGER PRIMARY KEY,
                                                                                    human_time TEXT,
                                                                                    day_of_week INTEGER,
                                                                                    tags TEXT,
                                                                                    x_res INTEGER,
                                                                                    y_res INTEGER,
                                                                                    heatmap TEXT);"""
        
        c.execute(sql_create_table)
        conn.close()
        
    def insert_data_into_db(self, d):
        # INSERT DATA
        conn = sqlite3.connect(self.data_base_name)
        c = conn.cursor()        
        sql_insert = 'INSERT OR REPLACE INTO ' + self.project + ' (date, human_time, day_of_week, tags, x_res, y_res, heatmap) VALUES (?,?,?,?,?,?,?)'        
        for p in range(0, len(d)):            
            c.execute(sql_insert, (d[p]['date'], d[p]['human_time'], d[p]['dayOfTheWeek'], d[p]['tags'], d[p]['x_res'], d[p]['y_res'], d[p]['heatmap']))
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