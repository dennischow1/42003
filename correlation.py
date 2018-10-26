# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 18:21:05 2018

@author: dchow
"""

from scipy.signal import correlate2d
from raw2ts import extract_time_series
import numpy as np
import csv
import os
import random
import itertools
import time

def import_data():
    station_list = []        
    with open("station_P98.txt",mode="r",newline='',encoding="utf-8") as f:
        csv_reader = csv.reader(f,delimiter=",")
        for row in csv_reader:
            station_list.append(row)
    fm_bus={}
    bus_list=[]
    #import fm_bus
    with open('KG/fm_bus',mode="r",newline='',encoding="utf-8") as f:
        csv_reader = csv.reader(f,delimiter=",")
        for row in csv_reader:
            fm_bus[row[0]]=row[1:]
            bus_list.append(row[0])
    
    fm_geo={}
    #import fm_geo
    with open('KG/fm_geo',mode="r",newline='',encoding="utf-8") as f:
        csv_reader = csv.reader(f,delimiter=",")
        for row in csv_reader:
            fm_geo[row[0]]=row[1:]
            
    retail2fuel={}
    with open('KG/retail2fuelbrand.txt',mode="r",newline='',encoding="utf-8") as f:
        csv_reader = csv.reader(f,delimiter=",")
        for row in csv_reader:
            retail2fuel[row[0]]=row[1]

    existing_ts = []
    for filename in os.listdir('station_fuelType/'):
        existing_ts.append(filename)

    return station_list,bus_list,fm_bus,fm_geo,existing_ts,retail2fuel

def test_ts(station_name,existing_ts):
    """
    Tests for time series data
    No more than 20 zeroes at the start
    """
    station_fuel = station_name+"_P98"
    if station_fuel not in existing_ts:
        extract_time_series(station_name,"P98")

    removed = 0
    s_data = np.loadtxt('station_fuelType/'+station_fuel,delimiter=',')
    s_y = s_data[:,1]
    while float(s_y[0]) == 0.0:
        removed = removed + 1
        s_y=s_y[1:len(s_y)]

    if removed > 20:
        return False
    else:
        return True
    
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
    
def intersect(s1,s2,bus_num,geo_num):
    """
    intersect of 2 stations
    """
    #business features
    intersect_features = []
    for f in range(0,bus_num):
        if int(s1[f]) == 0:
            intersect_features.append(0)
        elif s1[f] == s2[f]:
            intersect_features.append(1)
        else:
            intersect_features.append(0)
    
    #geographic feature
    for f in range(bus_num,bus_num+geo_num):
        if f == 249:
            intersect_features.append(min(float(s1[f])/float(s2[f]),float(s2[f])/float(s1[f])))
        elif f == 250:
            intersect_features.append(abs(int(s1[f])-int(s2[f])))
        else:
            if int(s1[f]) == 0:
                intersect_features.append(0)
            elif s1[f] == s2[f]:
                intersect_features.append(1)
            else:
                intersect_features.append(0)
    return intersect_features
    
def pop_fill(station_feat,station_max):
    """
    Entities missing population data replaced with average
    """    
    pop_index = 249
    pop_vals = station_feat[:,pop_index]
    pop_tot = 0
    pop_added = 0
    for val in pop_vals:
        if (not(int(val) == -1)) and (not(int(val) == 0)):
            pop_tot = pop_tot + int(val)
            pop_added=pop_added + 1
    
    pop_avg = pop_tot/pop_added
    
    for i in range(0,station_max):
        if (int(station_feat[i,pop_index]) == -1) or (int(station_feat[i,pop_index]) == 0):
            station_feat[i,pop_index] = pop_avg


if __name__ =='__main__':
    
    t_start = time.time()
    
    data_path = 'station_fuelType/'    
    file_list_path= data_path + 'filelist'
    
    station_list,bus_list,fm_bus,fm_geo,existing_ts,retail2fuel = import_data()    

    #shuffle station list
    random.shuffle(station_list)

    added = 0
    station_max = 50
    station2corr = []
    bus_num = 227
    geo_num = 44
    tot_feature = bus_num+geo_num #KG_bus features + KG_geo features
    station_feat = np.ndarray(shape=[0,tot_feature],dtype=float)

    tl_start = time.time()
    for station in station_list:
        if added <= station_max-1:
            bus = station[2]
            if bus in retail2fuel.keys():
                bus = retail2fuel[bus]
            #check business KG
            if bus in bus_list:
                #import time series
                if (station[0] not in station2corr) and (test_ts(station[0],existing_ts)):
#                    print("added:" + str(station[0]))
                    station2corr.append(station[0])
                    si_feat = np.hstack((np.array(fm_bus[bus]),np.array(fm_geo[station[0]])))
                    station_feat = np.vstack((station_feat,si_feat))
                    added = added + 1
        else:
            exit
    tl_end = time.time()
    
    
    pop_fill(station_feat,station_max)  #fill missing populations
    
    '''
    X FEATURES
    '''
    tx_start = time.time()
    
    features_x = np.ndarray(shape=[0,tot_feature])
    for s in itertools.combinations(range(0,station_max),2):
        compare = intersect(station_feat[s[0],:],station_feat[s[1],:],bus_num,geo_num)
        features_x = np.vstack((features_x,np.array(compare)))
    
    tx_end = time.time()    
    
    """
    Y FEATURES
    """
    ty_start = time.time()
    
    ts_y = equalise_ts(station2corr)
#    features_y = np.ndarray(shape=[0,1])
#    for s in itertools.combinations(range(0,station_max),2):

    
    ty_end = time.time()
    """
    PRINT DATA
    """
    with open('station2corr50r.txt', "w") as output_file:
        for i in range(0,len(station2corr)):
            output_file.write(str(station2corr[i])+'\n')
    output_file.closed

    with open('features_x50r.txt', "w") as output_file:
        for i in range(0,len(features_x)):
            for j in range (0,tot_feature-1):
                output_file.write(str(features_x[i][j])+',')
            output_file.write(str(features_x[i][tot_feature-1])+'\n')
    output_file.closed
    
    with open('ts50r_equalise.txt', "w") as output_file:
        for i in range(0,station_max):
            output_file.write(str(station2corr[i]))
            for val in ts_y[i,:]:
                output_file.write(','+str(val))
            output_file.write('\n')
    output_file.closed
    
    t_end = time.time()

    tx_total = tx_end-tx_start
    t_total = t_end-t_start
    tl_total = tl_end - tl_start
    print("run time: %.3fs" %t_total)
    print("list time: %.3fs" %tl_total)
    print("x feature time: %.3fs" %tx_total)
    
