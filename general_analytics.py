X = [0] * 24

count_ai = 0
count_code = 0
count_vr = 0
count_circulation = 0


ai_time = [0] * 24
code_time = [0] * 24
vr_time = [0] * 24

circulation_time = [0] * 24
exhibition_time = [0] * 24



time_index = 0
global_index = 0

for row in heat.iterrows():
    
    #print(str(time_index) + " - " + str(data[global_index][1]))
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

plt.xlabel('Hour', fontsize = 14)
plt.ylabel('Movement (%)', fontsize = 14)
plt.plot(X, circulation_time, color = 'red', lw = 4, label = 'circulation usage')
plt.plot(X, exhibition_time, color = 'blue', lw = 4, label = 'exhibition visit')
plt.legend()
plt.show()

plt.xlabel('Hour', fontsize = 14)
plt.ylabel('Movement (%)', fontsize = 14)
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