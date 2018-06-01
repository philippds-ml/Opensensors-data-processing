import math
import numpy as np
import matplotlib.pyplot as plt
import operator

########################## OUTLIERS ###################################################

class Outliers(object):
    
    def __init__(self, data):
        self.data = data
        self.outlier_index = []
        
        self.row_count = data['0'].count()
        self.outlier_flag = [0] * self.row_count
        self.column_count = len(data.columns)
        
        self.comptute()


        """
        for b in range(0, row_count):    
            temp_outlier_sum = 0
            for m in range(5, heatmap_length - 2 + 5):
                if (math.sqrt(math.pow(ave[m - 5] - data[b][m], 2)) > (ave[m - 5] * 1.5)):
                    temp_outlier_sum += 1
            outlier_sum.append(temp_outlier_sum)
        """
            
            
            
    # CALCULATE OUTLIERS
    def calc_outliers(self):
        outlier_pixel_sum = [0] * (self.column_count - 6)
        for r in range(6, self.column_count):
            # sort list
            sorted_list = []            
            for g in range(0, self.row_count):
                sorted_list.append(self.data.iat[g, r])
            sorted(sorted_list)
            # find lower and upper quartile and IQR
            rc = self.row_count
            x_025 = sorted_list[math.floor(rc * 0.25 + 1) - 1]
            x_075 = sorted_list[math.floor(rc * 0.75 + 1) - 1]
          
            iqr = x_075 - x_025            
            
            temp_outlier_sum = 0
            for m in range(0, self.row_count):
                if(self.data.iat[m, r] > (iqr * 1.5 + x_075) or self.data.iat[m, r] < (iqr * 1.5 + x_025)):
                    temp_outlier_sum += 1
                    self.outlier_flag[m] += 1
                    
            outlier_pixel_sum[r - 6] = temp_outlier_sum
            
        
        
        outlier_flag_sorted = sorted(self.outlier_flag)
        x_025 = outlier_flag_sorted[math.floor(rc * 0.25 + 1) - 1]
        x_075 = outlier_flag_sorted[math.floor(rc * 0.75 + 1) - 1]
        iqr = x_075 - x_025
        
        for a in range(0, self.row_count):
            if self.outlier_flag[a] > iqr * 1.5:
                self.outlier_index.append(a)
        
    
    # PLOT OUTLIERS
    def plot_heatmaps(self, index):

        arrs = []
        temp_arr = []
        count = len(index)
        
        for g in range(0, count):
            
            index_x = 0
            for m in range(6, self.column_count):
                if index_x == 38:
                    temp_arr.append(self.data.iat[index[g], m])
                    arrs.append(np.array(temp_arr))
                    temp_arr = []
                    index_x = 0
                    
                else:
                    temp_arr.append(self.data.iat[index[g], m])
                    index_x += 1
            
            heatmap_0 = np.array(arrs)
            
            col = 1
            row = 1
            
            if(count > 1):
                col = math.ceil(math.sqrt(count) * 1.2)
                row = math.ceil(count / col)
            
            plt.subplot(row, col, g + 1)
            plt.imshow(heatmap_0, cmap='hot', interpolation='gaussian')
     
            title = self.data.iat[index[g], 1] + " | " + str(self.outlier_flag[index[g]])        
            plt.title(title, loc = 'left', fontsize = 7)
            arrs = []
            temp_arr = []
            
            """
            for i in range(0, self.column_count - 6):
                if((i < 8) or ((i >= 39 and i % 39 < 8) and (int(i / 39) < 12))):
                    plt.scatter(i % 39, int(i / 39), color = 'blue', s = 10)
                
                if(int(i / 39) >= 18 and i % 39 > 10 and i % 39 <= 25 and (int(i / 39) < 21 or i % 39 > 15 or i % 39 < 12)):
                    plt.scatter(i % 39, int(i / 39), color = 'red', s = 10)
                
                if(int(i / 39) >= 10 and i % 39 > 25):
                    plt.scatter(i % 39, int(i / 39), color = 'green', s = 10)
            
            plt.scatter(7, 4, color = 'cyan', s = 30)
            plt.scatter(7, 14, color = 'cyan', s = 30)
            plt.scatter(18, 11, color = 'cyan', s = 30)
            """
            
            
    
        plt.show()
    
    def comptute(self):
        self.calc_outliers()
        
    def plot(self, count):
        
        out_flag = [0] * len(self.outlier_index)    
        for i in range(0, len(self.outlier_index)):
            out_flag[i] = self.outlier_flag[self.outlier_index[i]]
        
        top_dictionary = dict(zip(self.outlier_index, out_flag))
        top_dictionary = sorted(top_dictionary.items(), key = operator.itemgetter(1), reverse = True)

        outlier_index_cropped = []
        for k in top_dictionary:
            if len(outlier_index_cropped) == count:
                break
            outlier_index_cropped.append(k[0])
        
        self.plot_heatmaps(outlier_index_cropped)
        
        
        
        
        
        
        
        
        
        
        