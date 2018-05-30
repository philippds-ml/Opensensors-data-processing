

# CALC GOBAL AVERAGE
ave = []
for r in range(5, heatmap_length - 2 + 5):    
    value_sum = 0
    for g in range(0, row_count): 
        value_sum += int(data[g][r])
    ave.append(value_sum / row_count)


for b in range(0, row_count):    
    temp_outlier_sum = 0
    for m in range(5, heatmap_length - 2 + 5):
        if (math.sqrt(math.pow(ave[m - 5] - data[b][m], 2)) > (ave[m - 5] * 1.5)):
            temp_outlier_sum += 1
    outlier_sum.append(temp_outlier_sum)

# PLOT MULTIPLE HEATMAPS
def plot_heatmaps(input_data):
    
    number_of_heatmaps = len(input_data)
    
    col = math.ceil(math.sqrt(number_of_heatmaps) * 1.2)
    row = math.ceil(number_of_heatmaps / col)

    arrs = []
    temp_arr = []
    
    for g in range(0, number_of_heatmaps):
        
        index_x = 0
        for m in range(2, heatmap_length):
            if index_x == 38:
                temp_arr.append(int(input_data[g]['heatmap'][m]))
                arrs.append(np.array(temp_arr))
                temp_arr = []
                index_x = 0
                
            else:
                temp_arr.append(int(input_data[g]['heatmap'][m]))
                index_x += 1
        
        heatmap_0 = np.array(arrs)
        
        plt.subplot(row, col, g + 1)
        plt.imshow(heatmap_0, cmap='hot', interpolation='nearest')
 
        plt.title(input_data[g]['human_time'], loc = 'left', fontsize = 10)
        arrs = []
        temp_arr = []
    plt.show()    

plot_heatmaps(data[1:20])


# PLOT AVERAGE HEATMAP
number_of_heatmaps = len(data)
arrs = []
temp_arr = []
aaa = []

for g in range(0, number_of_heatmaps):
    index_x = 0
    for m in range(2, heatmap_length):
        if index_x == 38:
            temp_arr.append(int(data[g]['heatmap'][m]))
            arrs.append(np.array(temp_arr))
            temp_arr = []
            index_x = 0
        else:
            temp_arr.append(int(data[g]['heatmap'][m]))
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

