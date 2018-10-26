# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 09:47:00 2018

@author: DeSI-Anjin Liu
"""

import numpy as np

def load_ts_matrix(file_name, train_data_size = 366):
       
    with open(file_name) as f:
        content = f.readlines()
       
    id_dict = {}
    counter = 0
    
    ts_matrix = np.ndarray([0, len(content[0].split(','))-1], dtype=float )
    for line in content:
        values = line.replace('\n','').split(',')
        id_dict[counter] = values[0]
        ts_matrix = np.vstack([ts_matrix, np.array(values[1:], dtype = float)])
        counter = counter + 1

    ts_matrix = ts_matrix[:,:train_data_size]
    
    return ts_matrix, id_dict
    
def correlation_matrix(ts_matrix, lag = 0):
    
    m_size = ts_matrix.shape[0]
    
    corr_dict = {}
    for i in range(m_size-1):
        for j in range(i+1, m_size):
            corr = np.corrcoef(ts_raw_matrix[i,:], ts_raw_matrix[j,:])
            corr_dict[str(i)+'-'+str(j)] = corr[0, 1]
    return corr_dict

if __name__ == "__main__":
    
    lag = 0
    DataFile = 'ts50_equalise.txt'
    
    ts_raw_matrix, id_dict = load_ts_matrix(DataFile)
    
    corr_dict = correlation_matrix(ts_raw_matrix, lag)

    print(corr_dict)
    
    
    
    
    
    