import math
import numpy as np
import matplotlib.pyplot as plt

class Heatmap(object):
    
    def __init__(self, data):
        self.data = data     
        self.row_count = len(data.index)
        
        for i in range(0, self.row_count):
            heatmap_list = list(map(int, self.data.iat[i, 6].split(',')))
            for j in range(0, len(heatmap_list)):
                self.data.loc[i, j] = int(heatmap_list[i])
        
        self.data.drop('heatmap', axis=1, inplace=True)
        
        self.row_count = self.data['date'].count()
        self.column_count = len(self.data.columns)
        
        self.average = []
        self.average_heatmap = []
        self.calc_global_average()
        self.calc_average_heatmap()
        
        
        # plot_heatmaps(self.data[1:20])
    
    # CALC GOBAL AVERAGE
    def calc_global_average(self):
        ave = []
        for c in range(6, self.column_count):
            value_sum = 0
            for r in range(0, self.row_count):
                value_sum += int(self.data.iat[r, c])
            ave.append(value_sum / self.row_count)
        
        self.average = ave

    # PLOT MULTIPLE HEATMAPS
    def plot_heatmap_range(self, from_count, to_count):
        
        col = math.ceil(math.sqrt(to_count - from_count) * 1.2)
        row = math.ceil((to_count - from_count) / col)
    
        arrs = []
        temp_arr = []
        
        for r in range(from_count, to_count):
                        
            index_x = 0
            for c in range(6, self.column_count):
                if index_x == 38:
                    temp_arr.append(self.data.iat[r, c])
                    arrs.append(np.array(temp_arr))
                    temp_arr = []
                    index_x = 0
                    
                else:
                    temp_arr.append(self.data.iat[r, c])
                    index_x += 1
            
            heatmap_0 = np.array(arrs)
            plt.subplot(row, col, r - from_count + 1)
            plt.imshow(heatmap_0, cmap='hot', interpolation='gaussian')     
            plt.title(str(self.data.iat[r, 1]), loc = 'left', fontsize = 10)
            arrs = []
            temp_arr = []
    
        print("say something")
        plt.show()    

    def calc_average_heatmap(self):        
        arrs = []
        temp_arr = []
        aaa = []        
        
        print(self.row_count)
        print(self.column_count)
        print(self.data.iat[0, 4] - 1)
        
        """
        for r in range(0, self.row_count):
            index_x = 0
            for c in range(6, self.column_count):                
                if index_x == int(self.data.iat[r, 4] - 1):
                    temp_arr.append(self.data.iat[r, c])
                    arrs.append(np.array(temp_arr))
                    temp_arr = []
                    index_x = 0
                else:
                    
                    if not((int((c - 6) / 39) < 21 or (c - 6) % 39 > 15 or (c - 6) % 39 < 12)):
                        temp_arr.append(0)
                    else:
                    
                    temp_arr.append(self.data.iat[r, c])
                    index_x += 1
            
            if r == 0:
                aaa = np.array(arrs)
            else:
                aaa += np.array(arrs)
            
            arrs = []
            temp_arr = []
        """
        for r in range(0, self.row_count):
            if(r == 0):
                aaa = np.array(self.data[r,6:])
            else:
                aaa += np.array(self.data[r,6:])
        
            
        
        """
        for i in range(0, self.column_count - 6):
            if((i < 8) or ((i >= 39 and i % 39 < 8) and (int(i / 39) < 12))):
                plt.scatter(i % 39, int(i / 39), color = 'blue', s = 10)
            
            if(int(i / 39) >= 18 and i % 39 > 10 and i % 39 <= 25 and (int(i / 39) < 21 or i % 39 > 15 or i % 39 < 12)):
                plt.scatter(i % 39, int(i / 39), color = 'red', s = 10)
            
            if(int(i / 39) >= 10 and i % 39 > 25):
                plt.scatter(i % 39, int(i / 39), color = 'green', s = 10)
        """
        
        print(len(aaa))
        
        self.average_heatmap = aaa
    
    # PLOT AVERAGE HEATMAP
    def plot_average_heatmap(self):
        temp = 0
        print(len(self.average_heatmap))
        for r in range(0, self.row_count):
            temp = 0
            for c in range(6, self.column_count):
                temp += self.data.iat[r, c]
            print(temp)
        
        print(temp)
        plt.imshow(self.average_heatmap, cmap='hot', interpolation='nearest')
        plt.show()
