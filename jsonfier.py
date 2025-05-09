import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

np.set_printoptions(suppress=True,threshold=np.inf)
np.set_printoptions(linewidth=np.inf)
all_car_dict = np.load(r'E:\STU\Design\FaultDetection\five_fold_utils\all_car_dict.npz.npy',allow_pickle=True).item()
columns = ['volt', 'current', 'soc', 'max_single_volt', 'min_single_volt', 'max_temp', 'min_temp', 'timestamp']
car_data = {}


def read_car_data(car_num):
    print("Processing car_num :", car_num)
    car_data[car_num] = {}
    car_path = all_car_dict[car_num]

    #load the segments
    for pathnum in car_path:
        data = torch.load(pathnum)
        '''
        the data structure is:
            data[0] = [n*[volt, current, soc, max_single_volt, min_single_volt, max_temp, min_temp, timestamp]]
            data[1] = {label,car,,charge_segment,mileage}
        '''
        #add the charge_segment number to list
        if data[1]['charge_segment'] not in car_data[car_num]:
            car_data[car_num][int(data[1]['charge_segment'])]=[]
            #print("segment:",data[1]['charge_segment'])

        #add the data of a chage_segment into the list
        for charging_data in data[0]:
            car_data[car_num][int(data[1]['charge_segment'])].append(charging_data.tolist())

    #sort the segments and generate json files
    for segment in car_data[car_num]:
        #print(segment)
        car_data[car_num][segment].sort(key=lambda x: x[2])
        car_data[car_num][segment]=np.array(car_data[car_num][segment])

        #save the volt\current\soc
        for i in range(3):
            column_name = columns[i]
            json_data = []
            for row in car_data[car_num][segment]:
                value = row[i]
                time_value = row[-1]
                entry = {
                    column_name: value,
                    "time": time_value,
                    "s":"1"
                }
                json_data.append(entry)
            file_name = f"output/{column_name}/{car_num}_{segment}.json"
            with open(file_name, 'w') as f:
                json.dump(json_data, f, indent=4)
            #print(f"Data for {column_name} saved to {file_name}")
        
        #save the single_volt,temp
        for i in range(3,6):
            column_name = columns[i]
            json_data = []
            for row in car_data[car_num][segment]:
                value1 = row[i]
                time_value = row[-1]
                entry = {
                    column_name: value1,
                    "time": time_value,
                    "s":"max"
                }
                json_data.append(entry)

                value = row[i + 1]
                entry = {
                    column_name: value,
                    "time": time_value,
                    "s":"min"
                }
                json_data.append(entry)

            file_name = f"output/{column_name}/{car_num}_{segment}.json"
            with open(file_name, 'w') as f:
                json.dump(json_data, f, indent=4)
            #print(f"Data for {column_name} saved to {file_name}")
            i+=1
    
# used for plotting and debugging
'''
pkl_file = torch.load('your_pkl_file.pkl')
time_series_data = pkl_file[0]
column_names = torch.load('column.pkl')
df = pd.DataFrame(car_data[31][177], columns=columns)
timestamp = df.iloc[:, 7]
voltage = df['volt']
current = df['current']
soc = df['soc']

plt.figure(figsize=(12, 6))
plt.subplot(3, 1, 1)
plt.plot(timestamp, voltage, label='Voltage')
plt.xlabel('Time (s)')
plt.ylabel('Voltage')
plt.title('Voltage over Time')
plt.legend()
plt.subplot(3, 1, 2)
plt.plot(timestamp, current, label='Current', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Current')
plt.title('Current over Time')
plt.legend()
plt.subplot(3, 1, 3)
plt.plot(timestamp, soc, label='SOC', color='red')
plt.xlabel('Time (s)')
plt.ylabel('SOC')
plt.title('SOC over Time')
plt.legend()
plt.tight_layout()
plt.show()
#print(car_data[31][177])
'''
if __name__ == '__main__':
    read_car_data(214)  
    read_car_data(231)
    read_car_data(233)  


