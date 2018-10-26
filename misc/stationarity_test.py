# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 20:16:15 2018

@author: dchow
"""

from statsmodels.tsa.stattools import adfuller
import numpy as np
import csv

def adfuller_test(data):
    """
    Augmented Dickey-Fuller test
    """
    result = adfuller(data)
    print('Augmented Dickey-Fuller Test')
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Used lag: %i' % result[2])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))

if __name__ =='__main__':
    data_path = 'evaluation_stream/'    
    file_list_path= data_path + 'filelist'
    file_list = []
    results_file = 'stationarity_results.txt'
    
    with open(file_list_path) as f:
        for line in f:
            file_list.append(line.replace('\n',''))
    
    adfuller_results={}
    for s in file_list:
        s_data = np.loadtxt(data_path+s,delimiter=',')
        s_y = s_data[:,1]
        s_y_size = s_y.shape[0]
        result = adfuller(s_y) #augmented Dickey-Fuller test
        adfuller_results[s]=[float(result[0]),float(result[1]),result[2],result[3],float(result[5])]
    
    with open(results_file,mode="w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",",quotechar="'")
        writer.writerow(['adf stat','p-value','used lag','nobs','icbest'])
        for s in adfuller_results:
            writer.writerow([s,','.join(map(str,adfuller_results[s]))])
    
# =============================================================================
#     for s in adfuller_results:
#         print(s)
#         for result in adfuller_results[s]:
#             print(result)
#             #print(type(result))
# =============================================================================
            
