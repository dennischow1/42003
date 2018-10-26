# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 19:30:55 2018

@author: dchow and Anjin Liu
"""

import numpy as np
from sklearn.linear_model import BayesianRidge
import matplotlib.pyplot as plt
import time

def data_preprocessing(file_list):

    
    s_y={}
    s_y_size = 1254 #truncate to 1254 data
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

def MSE_Bay(train_data,lag,t_ahead):
    sample_x = np.transpose(train_data[:,:-lag])
    
    for i in range(1, lag):
        sample_x = np.hstack([sample_x, np.transpose(train_data[:,i:-(lag-i)])])
    
    sample_x = sample_x[:-t_ahead,:]
    
    num_stream = 1
    slding_predict_t = 366
    landmark_win_ini_size = 1
    for s_i in range(num_stream):
        sample_y_si = np.transpose(train_data[s_i,t_ahead+lag-1:])
#        print(sample_y_si[367])
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
            
#        plt.plot(range(landmark_win_ini_size+1,landmark_win_ini_size+landmark_win+2),pre_y,label='prediction s'+str(s_i))
#        plt.plot(range(landmark_win_ini_size+1,landmark_win_ini_size+landmark_win+2),act_y,label='actual')
#        plt.legend()
#        plt.show()
#        print(pre_y)
#        print(act_y)
        MSE = 0
        for i in range (0,len(pre_y)):
            if not(np.isnan(pre_y[i])): 
                MSE = MSE + (pre_y[i]-act_y[i])**2
#        pre = np.array(pre_y)
#        act = np.array(act_y)
#        print(np.sum(pre-act))
        return MSE


if __name__ =='__main__':
    
    t_start = time.time()
    data_path = 'evaluation_stream/'    
    file_list_path= data_path + 'filelist'
    file_list = []
    
    with open(file_list_path) as f:
        for line in f:
            file_list.append(line.replace('\n',''))
            
    s_y = data_preprocessing(file_list)
    
    train_data = np.ndarray(shape=[0, 1254], dtype = 'float')
    for key, v in s_y.items():
        train_data = np.vstack([train_data, np.array(v)])
    
#    lag = 2
#    t_ahead = 7 #t_ahead = target training value
  
    lag1 = 1
    lag2 = 10
    t_ahead1=1  #first t_ahead
    t_ahead2=14 #last t_ahead
    
    MSE = np.ndarray(shape=[0,t_ahead2],dtype='float')
    
    for lag in range(lag1,lag2+1):
        MSE_list = []
        for t_ahead in range(t_ahead1,t_ahead2+1):
            MSE_list.append(MSE_Bay(train_data,lag,t_ahead))
#        print(MSE_list)
        MSE = np.vstack((MSE,np.transpose(np.array(MSE_list))))
        
    t_end = time.time()

    with open('evaluation_results_BRR.txt', "w") as output_file:
        for lag in range(lag1,lag2+1):
            output_file.write(str(lag))
            for t_ahead in range (t_ahead1,t_ahead2+1):
                output_file.write(',' + str(MSE[lag-lag1,t_ahead-t_ahead1]))
            output_file.write('\n')
    output_file.closed
    
    t_total = t_end - t_start
    print('runtime: %.3f' %t_total)
#    with open('evaluation_results_BRR', 'w') as output_file:
#        for lag in range(2,11):
#            output_file.write(str(lag))
#            for t_ahead in range (1,15):
#                output_file.write(',' + str(MSE[lag-2,t_ahead-1]))
#            output_file.write('\n')
#    output_file.closed

    
    
    
        
    
    