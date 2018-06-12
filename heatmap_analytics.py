import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse
from scipy import ndimage

class Heatmap(object):
    
    def __init__(self, data = pd.DataFrame()):
        self.data = data
        self.x_res = data.iat[0, 4]        
        self.row_count = len(data.index)
        self.column_count = len(self.data.columns)
        self.average_heatmap = []
        self.calc_average_heatmap()
    
    # PLOT MULTIPLE HEATMAPS
    def plot_heatmap_range(self, from_count, to_count):               
        col = math.ceil(math.sqrt(to_count - from_count) * 1.2)
        row = math.ceil((to_count - from_count) / col)
        
        arrs = []
        temp_arr = []
        
        for r in range(from_count, to_count):                        
            index_x = 0
            for c in range(6, self.column_count):
                if index_x == self.x_res - 1:
                    temp_arr.append(self.data.iat[r, c])
                    arrs.append(np.array(temp_arr))
                    temp_arr = []
                    index_x = 0
                    
                else:
                    temp_arr.append(self.data.iat[r, c])
                    index_x += 1
            
            heatmap = np.array(arrs)
            plt.subplot(row, col, r - from_count + 1)
            plt.imshow(heatmap, cmap='hot', interpolation='gaussian')     
            plt.title(str(self.data.iat[r, 1]), loc = 'left', fontsize = 10)
            arrs = []
            temp_arr = []
        plt.show()

    def plot_heatmap_stime(self, from_count, to_count, time):        
        count = 0
        indexes = []
        for r in range(from_count, to_count):
            if time == 0:
                if parse(self.data.iat[r, 1]).hour % time == 0:
                    count += 1
                    indexes.append(r)
            else:
                if parse(self.data.iat[r, 1]).hour % time == 0 and parse(self.data.iat[r, 1]).hour != 0:
                    count += 1
                    indexes.append(r)
        
        print(indexes)
        print(count)
        
        col = math.ceil(math.sqrt(count) * 1.2)
        print(col)
        row = math.ceil(count / col)
        print(row)
        
        arrs = []
        temp_arr = []
        
        for r in range(0, count):
            index_x = 0
            for c in range(6, self.column_count):                
                if index_x == self.x_res - 1:
                    temp_arr.append(self.data.iat[indexes[r], c])
                    arrs.append(np.array(temp_arr))
                    temp_arr = []
                    index_x = 0
                    
                else:
                    temp_arr.append(self.data.iat[indexes[r], c])
                    index_x += 1
        
        
            img = np.array(arrs)
            nrows, ncols = img.shape
            pixel_blur_factor = 4
            sigma = (pixel_blur_factor * nrows / 100.0, pixel_blur_factor * ncols / 100.0)
            img = ndimage.gaussian_filter(img, sigma=sigma)

            plt.subplot(row, col, r + 1)
            plt.imshow(img, cmap='hot', interpolation='gaussian') 
            
            plt.title(str(self.data.iat[indexes[r], 1]), loc = 'left', fontsize = 10)
            arrs = []
            temp_arr = []
        plt.show()
    
    def calc_average_heatmap(self):
        average = []
        for r in range(0, self.row_count):
            if(r == 0):
                average = np.array(self.data.iloc[r,6:])
            else:
                average += np.array(self.data.iloc[r,6:])
                
        heatmap = []
        temp_arr = []
        index_x = 0
        for c in range(0, self.column_count - 6):            
            if index_x == self.x_res - 1:
                temp_arr.append(average[c] / self.row_count)
                heatmap.append(np.array(temp_arr))
                temp_arr = []
                index_x = 0                
            else:
                temp_arr.append(average[c] / self.row_count)
                index_x += 1
        
        self.average_heatmap = np.array(heatmap)
        
        # PLOT AVERAGE HEATMAP
    def plot_average_heatmap(self):
        img = self.average_heatmap
        nrows, ncols = img.shape
        pixel_blur_factor = 4
        sigma = (pixel_blur_factor * nrows / 100.0, pixel_blur_factor * ncols / 100.0)
        img = ndimage.gaussian_filter(img, sigma=sigma)
        
        plt.imshow(img, cmap='hot', interpolation='gaussian')
        plt.show()
    
    def plot_area_scatter(self):        
        if self.data.iat[0, 3] == 'AUB':
            for i in range(0, self.column_count - 6):
                if((i < 8) or ((i >= 39 and i % 39 < 8) and (int(i / 39) < 12))):
                    plt.scatter(i % 39, int(i / 39), color = 'blue', s = 10)
                
                if(int(i / 39) >= 18 and i % 39 > 10 and i % 39 <= 25 and (int(i / 39) < 21 or i % 39 > 15 or i % 39 < 12)):
                    plt.scatter(i % 39, int(i / 39), color = 'red', s = 10)
                
                if(int(i / 39) >= 10 and i % 39 > 25):
                    plt.scatter(i % 39, int(i / 39), color = 'green', s = 10)
        """ 
        if self.data.iat[r, 3] == 'Reception':
            # Reception Scatter
        if self.data.iat[r, 3] == 'Meeting':
            # Meeting Scatter
        """
        
        