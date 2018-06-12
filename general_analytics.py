import matplotlib.pyplot as plt
from dateutil.parser import parse
import pandas as pd
import math

########################## GENERAL ANALYTICS ###################################################

class General(object):
        
    def __init__(self, data = pd.DataFrame()):
        self.data = data
        self.heatmap_series = data.iloc[:,6:7]
        
        self.row_count = data.shape[0]
        self.column_count = self.data.shape[1]
        
        self.day_count = 0
        self.week_count = 0
        self.month_count = 0
        
                    # AI
                    # CODE
                    # VR
                    # CIRCULATION
                    # EXHIBITION
        
        self.AUB_dictionary = {'ai': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                               'code': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                               'vr': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                               'circulation': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                               'exhibition': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31}}

                    # CIRCULATION
                    # MEETING TABLE
                    # SITTING TABLES
                    # STANDING TABLES
                    # CAFE BAR
                    # RECEPTION
                    # CIRCULATION
                    
        self.Reception_dictionary = {'meeting': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                                     'sitting': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                                     'standing': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                                     'cafe': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                                     'reception': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                                     'circulation': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31}}
        
                    # MEETING CHAIRS FRONT Quarter
                    # MEETING CHAIRS FRONT HALF
                    # MEETING CHAIRS FRONT Three Quater
                    # MEETING CHAIRS FRONT TOTAL
                    # CIRCULATION
                    # MEETING
                    
        self.Meeting_dictionary = {'quarter': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                                   'half': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                                   'three': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                                   'total': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                                   'circulation': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31},
                                   'meeting': {'count': 0, 'day': [0] * 24, 'week': [0] * 7, 'month': [0] * 31}}

        self.count_ai = 0
        self.count_code = 0
        self.count_vr = 0
        self.count_circulation = 0
        self.count_exhibition = 0
        
        self.ai_day = [0] * 24
        self.code_day = [0] * 24
        self.vr_day = [0] * 24        
        self.circulation_day = [0] * 24
        self.exhibition_day = [0] * 24
        
        self.ai_week = [0] * 7
        self.code_week = [0] * 7
        self.vr_week = [0] * 7
        self.circulation_week = [0] * 7
        self.exhibition_week = [0] * 7
        
        self.ai_month = [0] * 31
        self.code_month = [0] * 31
        self.vr_month = [0] * 31     
        self.circulation_month = [0] * 31
        self.exhibition_month = [0] * 31
        
        self.count_all_movement()
        print("ai", self.count_ai, "code", self.count_code, "vr", self.count_vr)
        #self.calculate_movement_over_time(data)
        

    def count_all_movement(self):
        for r in range(0, self.row_count):
            for c in range(0, self.column_count - 6):
                value = self.data.iat[r, c + 6]
                
                if(self.data.iat[r, 3] == 'AUB'):
                    if((c < 8) or (c >= 39 and c % 39 < 8) and (int(c / 39) < 12)):
                        self.count_ai += value
                        self.count_exhibition += value
                    elif(int(c / 39) >= 18 and c % 39 > 10 and c % 39 <= 25):
                        self.count_code += value
                        self.count_exhibition += value
                    elif(int(c / 39) >= 10 and c % 39 > 25):
                        self.count_vr += value
                        self.count_exhibition += value
                    else:
                        self.count_circulation += value
                """
                if(self.data.iat[r, 3] == 'Reception'):
                    # CIRCULATION
                    # MEETING TABLE
                    # SITTING TABLES
                    # STANDING TABLES
                    # CAFE BAR
                    # RECEPTION
                    
                if(self.data.iat[r, 3] == 'Meeting'):
                    # MEETING CHAIRS
                    # CIRCULATION
                    # MEETING
                """

    # TO DO:
    def calculate_movement_over_time(self, data):
        day_index = 0
        week_index = 0
        month_index = 0
        
        for r in range(0, self.row_count):
            circulation_temp = 0            
            exhibition_temp = 0       
            ai_temp = 0
            code_temp = 0
            vr_temp = 0

            for c in range(0, self.column_count - 6):
                value = data.iat[r, c + 6]
                if((c < 8) or ((c >= 39 and c % 39 < 8) and (int(c / 39) < 12))):
                    exhibition_temp += value
                    ai_temp += value
                elif(int(c / 39) >= 18 and c % 39 > 10 and c % 39 <= 25):
                    exhibition_temp += value
                    code_temp += value
                elif(int(c / 39) >= 10 and c % 39 > 25):
                    exhibition_temp += value
                    vr_temp += value
                else:
                    circulation_temp += value
            
            self.circulation_day[day_index] += circulation_temp
            self.exhibition_day[day_index] += exhibition_temp
            self.ai_day[day_index] += ai_temp
            self.code_day[day_index] += code_temp
            self.vr_day[day_index] += vr_temp
            
            week_index = data.iat[r, 2]             
            self.circulation_week[week_index] += circulation_temp
            self.exhibition_week[week_index] += exhibition_temp
            self.ai_week[week_index] += ai_temp
            self.code_week[week_index] += code_temp
            self.vr_week[week_index] += vr_temp
            
            month_index = parse(data.iat[r, 1]).date().day - 1
            self.circulation_month[month_index] += circulation_temp
            self.exhibition_month[month_index] += exhibition_temp
            self.ai_month[month_index] += ai_temp
            self.code_month[month_index] += code_temp
            self.vr_month[month_index] += vr_temp
            
            if(day_index < 23):
                day_index += 1
            else:
                day_index = 0
                self.day_count += 1                
        
        for i in range(0, len(self.ai_day)):
            self.ai_day[i] /= self.day_count
            self.code_day[i] /= self.day_count
            self.vr_day[i] /= self.day_count     
            self.circulation_day[i] /= self.day_count
            self.exhibition_day[i] /= self.day_count
        
        for i in range(0, len(self.ai_week)):
            week_count = math.ceil(self.day_count / 7)
            self.ai_week[i] /= week_count
            self.code_week[i] /= week_count
            self.vr_week[i] /= week_count
            self.circulation_week[i] /= week_count
            self.exhibition_week[i] /= week_count
            
        for i in range(0, len(self.ai_month)):
            month_count = math.ceil(self.day_count / 31)
            self.ai_month[i] /= month_count
            self.code_month[i] /= month_count
            self.vr_month[i] /= month_count    
            self.circulation_month[i] /= month_count
            self.exhibition_month[i] /= month_count
   
    def period_plot(self, period, kind):
        title = ""
        
        if(period == 'day'):
            title = "AUB Movement Data | Average Day"
            plt.xlabel('Hours', fontsize = 14)
            X = [i for i in range(24)]
            if(kind == 'circulation'):  plt.plot(X, self.circulation_day, color = 'coral', lw = 4, label = 'circulation usage')
            if(kind == 'exhibition'):  plt.plot(X, self.exhibition_day, color = 'blue', lw = 4, label = 'exhibition visits')
            if(kind == 'ai'):  plt.plot(X, self.ai_day, color = 'lightblue', lw = 4, label = 'ai visits')
            if(kind == 'code'):  plt.plot(X, self.code_day, color = 'teal', lw = 4, label = 'code visits')
            if(kind == 'vr'):  plt.plot(X, self.vr_day, color = 'turquoise', lw = 4, label = 'vr visits')
        if(period == 'week'):
            title = "AUB Movement Data | Average Week"
            plt.xlabel('Days', fontsize = 14)
            X = [i for i in range(1, 8)]
            if(kind == 'circulation'):  plt.plot(X, self.circulation_week, color = 'coral', lw = 4, label = 'circulation usage')
            if(kind == 'exhibition'):  plt.plot(X, self.exhibition_week, color = 'blue', lw = 4, label = 'exhibition visits')
            if(kind == 'ai'):  plt.plot(X, self.ai_week, color = 'lightblue', lw = 4, label = 'ai visits')
            if(kind == 'code'):  plt.plot(X, self.code_week, color = 'teal', lw = 4, label = 'code visits')
            if(kind == 'vr'):  plt.plot(X, self.vr_week, color = 'turquoise', lw = 4, label = 'vr visits')
        if(period == 'month'):
            title = "AUB Movement Data | Average Month"
            plt.xlabel('Days', fontsize = 14)
            X = [i for i in range(1, 32)]
            if(kind == 'circulation'):  plt.plot(X, self.circulation_month, color = 'coral', lw = 4, label = 'circulation usage')
            if(kind == 'exhibition'):  plt.plot(X, self.exhibition_month, color = 'blue', lw = 4, label = 'exhibition visits')
            if(kind == 'ai'):  plt.plot(X, self.ai_month, color = 'lightblue', lw = 4, label = 'ai visits')
            if(kind == 'code'):  plt.plot(X, self.code_month, color = 'teal', lw = 4, label = 'code visits')
            if(kind == 'vr'):  plt.plot(X, self.vr_month, color = 'turquoise', lw = 4, label = 'vr visits')
        
        plt.title(title, loc = 'left', fontsize = 20)
        plt.ylabel('Movement in Seconds', fontsize = 14)
        plt.legend()
        plt.show()
    
    def plot_comparison_bars(self):
        title = "AUB Movement Data | Total Movement Count"
        plt.title(title, loc = 'left', fontsize = 20)
        X = [i for i in range(5)]
        colors = ['coral', 'blue', 'lightblue', 'teal', 'turquoise']
        plt.ylabel('Movement in Seconds (k)', fontsize = 14)
        plt.bar(X, [self.count_circulation, self.count_exhibition, self.count_ai, self.count_code, self.count_vr], color = colors)
        plt.xticks(X, ('Circulation', 'Exhibition','AI', 'CODE', 'VR'))
        plt.show()
        