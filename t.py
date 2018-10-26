# -*- coding: utf-8 -*-
from raw2ts import extract_time_series

fileName='station_name'
station_list = []
fuel_type = []
with open(fileName) as f:
    for line in f:
        station_list.append(line.replace('\n',''))

fileName='fuel_type'            
with open(fileName) as f:
    for line in f:
        fuel_type.append(line.replace('\n',''))

for station in station_list:
    for ftype in fuel_type:
        extract_time_series(station, ftype)
