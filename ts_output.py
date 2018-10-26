# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:46:56 2018

@author: dchow
"""

import numpy as np

def equalise_ts(station_list):
    """
    Makes all time series equal in length with no zeroes
    """
    s_y={}
    s_y_size = 5000 #large number for first pass
    for s in station_list:
        s_data = np.loadtxt('station_fuelType/'+s+"_P98",delimiter=',')
        s_y[s] = s_data[:,1]
        while float(s_y[s][0]) == 0.0:
            s_y[s]=s_y[s][1:len(s_y[s])]
        if len(s_y[s])<s_y_size:
            s_y_size = len(s_y[s])
    
    for s in s_y:
        if len(s_y[s])>s_y_size:
            s_y[s]=s_y[s][len(s_y[s])-s_y_size:len(s_y[s])]
            
    ts_y = np.ndarray(shape=[0, s_y_size], dtype = 'float')
    for key, v in s_y.items():
        ts_y = np.vstack([ts_y, np.array(v)])

    return ts_y


if __name__ =='__main__':
    station_list = []
    with open('station2corr.txt') as f:
        for line in f:
            station_list.append(line.replace('\n',''))

    #ts_y = equalise_ts(station_list)
    
    s_y={}
    s_y_size = 5000 #large number for first pass
    counter = 1
    for s in station_list:
        s_data = np.loadtxt('station_fuelType/'+s+"_P98",delimiter=',')
        if s in s_y.keys():
            print(s)
        s_y[s] = s_data[:,1]
        while float(s_y[s][0]) == 0.0:
            s_y[s]=s_y[s][1:len(s_y[s])]
        if len(s_y[s])<s_y_size:
            s_y_size = len(s_y[s])
    
    for s in s_y:
        if len(s_y[s])>s_y_size:
            s_y[s]=s_y[s][len(s_y[s])-s_y_size:len(s_y[s])]
            
    ts_y = np.ndarray(shape=[0, s_y_size], dtype = 'float')
    for key, v in s_y.items():
        ts_y = np.vstack([ts_y, np.array(v)])

    with open('ts_200_equalise.txt', "w") as output_file:
        for i in range(0,len(station_list)):
            output_file.write(str(station_list[i]))
            for val in ts_y[i,:]:
                output_file.write(','+str(val))
            output_file.write('\n')
    output_file.closed