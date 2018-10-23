# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 19:30:55 2018

@author: dchow 
"""

import numpy as np
from scipy import stats
from sklearn.linear_model import BayesianRidge, LinearRegression
import matplotlib.pyplot as plt

def data_preprocessing(file_list):

    
    s_y={}
    s_y_size = 5000 #large number for first pass
    for s in file_list:
        s_data = np.loadtxt(data_path+s,delimiter=',')
        s_y[s] = s_data[:,1]
        while float(s_y[s][0]) == 0.0:
            s_y[s]=s_y[s][1:len(s_y[s])]
        if len(s_y[s])<s_y_size:
            s_y_size = len(s_y[s])
    

    for s in s_y:
        if len(s_y[s])>s_y_size:
            s_y[s]=s_y[s][len(s_y[s])-s_y_size:len(s_y[s])]
            
    return s_y

if __name__ =='__main__':
    data_path = 'evaluation_stream/'    
    file_list_path= data_path + 'filelist'
    file_list = []
    
    with open(file_list_path) as f:
        for line in f:
            file_list.append(line.replace('\n',''))
            
    s_y = data_preprocessing(file_list)
    
#    X = np.ndarray(shape=(59,11))
#    X_temp = []
    
    '''
    for i in range(0,59):
        X_temp = []
        for s in s_y:
            X_temp.append(s_y[s][i])
        X_temp.append(s_y[file_list[0]][i+1])
        X_temp= np.array(X_temp)
        X = np.concatenate((X,X_temp))
    '''
    train_data = np.ndarray(shape=[0, 1256], dtype = 'float')
    for key, v in s_y.items():
        train_data = np.vstack([train_data, np.array(v)])
        
    lag = 2
    t_ahead = 10
    sample_x = np.transpose(train_data[:,:-lag])
    
    for i in range(1, lag):
        sample_x = np.hstack([sample_x, np.transpose(train_data[:,i:-(lag-i)])])
    
    sample_x = sample_x[:,:-t_ahead]
    
    num_stream = 1
    slding_predict_t = 1000
    landmark_win_ini_size = 60
    for s_i in range(num_stream):
        sample_y_si = np.transpose(train_data[0,t_ahead:-lag])
        reg_si = BayesianRidge()
        pre_y = []
        act_y = []
        for landmark_win in range(slding_predict_t):
            train_x = sample_x[:landmark_win_ini_size+landmark_win,:]
            train_y = sample_y_si[:landmark_win_ini_size+landmark_win]
            reg_si.fit(train_x,train_y)
            y_hat = reg_si.predict(sample_x[landmark_win_ini_size+landmark_win:landmark_win_ini_size+landmark_win+1,:])
            pre_y.append(y_hat)
            act_y.append(sample_y_si[landmark_win_ini_size+landmark_win:landmark_win_ini_size+landmark_win+1])
            
            
        plt.plot(pre_y)
        plt.plot(act_y)
        plt.show()
        pre = np.array(pre_y)
        act = np.array(act_y)
        print(np.sum(pre-act))
    
    
#    sample_x_s0 = train_data[:,0]
#    sample_y_s0 = train_data[0,1]
#    
#    sample_s1 = np.hstack([sample_x_s1, sample_y_s1])
    
    
    
    
    #train_data = np.transpose(train_data)
    
    

    
    
    
        
    
    