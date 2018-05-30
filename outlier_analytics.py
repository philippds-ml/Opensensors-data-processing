
########################## OUTLIERS ###################################################

# CALCULATE OUTLIERS
def calc_outliers(data):
    outlier_pixel_sum = []
    outlier_flag = [0] * row_count
    #outlier_sum = []
    
    for r in range(2, heatmap_length):
        # sort list
        sorted_list = []
        for g in range(0, row_count):
            sorted_list.append(data[g]['heatmap'][r])
        sorted(sorted_list)
        
        # find lower and upper quartile and IQR
        x_025 = sorted_list[math.floor(row_count * 0.25 + 1) - 1]
        x_075 = sorted_list[math.floor(row_count * 0.75 + 1) - 1]
        
        iqr = x_075 - x_025
        
        
        temp_outlier_sum = 0
        for m in range(0, row_count):
            #if data[m][r] > iqr * 1.5:
            if(data[m]['heatmap'][r] > (iqr * 1.5 + x_075) or data[m]['heatmap'][r] < (iqr * 1.5 + x_025)):
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
    
    return outlier_index

def plot_heatmaps(indexes, count, col):
    #plt.title(data[][])    
    # number_of_heatmaps = len(indexes)
    arrs = []
    temp_arr = []
    
    for g in range(0, count):
        
        index_x = 0
        for m in range(2, heatmap_length):
            if index_x == 38:
                temp_arr.append(data[indexes[g]]['heatmap'][m])
                arrs.append(np.array(temp_arr))
                temp_arr = []
                index_x = 0
                
            else:
                temp_arr.append(data[indexes[g]]['heatmap'][m])
                index_x += 1
        
        heatmap_0 = np.array(arrs)
        
        plt.subplot(math.ceil(count / col), col, g + 1)
        plt.imshow(heatmap_0, cmap='hot', interpolation='gaussian')
 
        title = data[indexes[g]]['human_time'] + " | " + str(outlier_flag[indexes[g]])
    
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

# PLOT OUTLIER HEATMAPs
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
