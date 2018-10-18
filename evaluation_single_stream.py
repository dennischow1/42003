# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 19:31:28 2018

@author: DeSI-Anjin, Dennis Chow
"""

#from sklearn.linear_model import BayesianRidge, LinearRegression
#from sklearn import linear_model
import numpy as np
from statsmodels.tsa.ar_model import AR
from random import random
from matplotlib import pyplot as plt

data_path = 'evaluation_stream/'

file_list_path= data_path + 'filelist'
file_list = []
with open(file_list_path) as f:
    for line in f:
        file_list.append(line.replace('\n',''))

predict_period = 14
#reg = linear_model.BayesianRidge()
for s in file_list:
    s_data = np.loadtxt(data_path+s,delimiter=',')
    s_y = s_data[:,1]
    s_y_size = s_y.shape[0]
    model = AR(s_y)
    model_fit = model.fit()
    yhat = model_fit.predict(len(s_y), len(s_y))
    plt.plot(s_y)
    plt.plot(yhat)
    
plt.show()
# =============================================================================
#     for slide in range(100, s_y_size - predict_period):
#         print (slide)
#         X = s_y[:slide]
#         Y = s_y[slide:slide+predict_period]
#         model = AR(X)
#         model_fit = model.fit()
#         yhat = model_fit.predict(len(data), len(data))
#     print(s_y_size)
#     
#     # contrived dataset
#     data = [x + random() for x in range(1, 100)]
#     # fit model
#     model = AR(data)
#     model_fit = model.fit()
#     # make prediction
#     yhat = model_fit.predict(len(data), len(data))
# =============================================================================
    
    
    
    
    