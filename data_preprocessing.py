import pandas as pd

def preprocess(data):
    data_dictionary = {}
    data2 = []
    heatmap_series = data.iloc[:,6:7]
    row_count = data.shape[0]
    for i in range(0, row_count):            
        temp = heatmap_series.iat[i, 0].split(',')
        heatmap_list = []
        for j in range(0, len(temp)):
            heatmap_list.append(int(temp[j]))                    
        data2.append(heatmap_list)

    for i in range(0, len(data2)):
        data_dictionary[i] =  data2[i]
    
    data2 = pd.DataFrame(data = data_dictionary).T

    
    data = pd.concat([data, data2], axis = 1)
    data = data.drop(columns='heatmap')
    return data