# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 19:31:28 2018

@author: DeSI-Anjin, Dennis Chow
"""

#from sklearn.linear_model import BayesianRidge, LinearRegression
#from sklearn import linear_model
import numpy as np
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARIMA
#from statsmodels.tsa.stattools import adfuller,acf,pacf
#from random import random
#from matplotlib import pyplot as plt
#from pandas.plotting import autocorrelation_plot
#from statsmodels.graphics.tsaplots import plot_acf
import csv


def AR_model(s_y):
    model = AR(s_y)
    model_fit = model.fit(maxlag = 50)
    yhat = model_fit.predict(100, len(s_y))
    yhat = np.hstack([np.zeros([99]), yhat])


def ARIMA_model(s_y,p,q,d):
    """
    Run ARIMA model for p,q,d
    Return:-
    Predicted values (yhat)
    Akaike information criterion (aic)
    Mean Squared Error (MSE)
    """
    model = ARIMA(s_y,order=(p,q,d))
    try:
        model_fit = model.fit(disp=False)
        if q == 0:
            yhat = model_fit.predict(q, len(s_y))
        else:    
            yhat = model_fit.predict(q, len(s_y), typ='levels')
        
        aic = model_fit.aic
        MSE = 0
        for i in range(q,len(s_y)-1):
            MSE = MSE + (yhat[i]-s_y[i])**2
            i=i+1
    except ValueError:
        yhat=[]
        MSE=0
        aic=0

    return [yhat,MSE,aic]

if __name__ =='__main__':
    data_path = 'evaluation_stream/'    
    file_list_path= data_path + 'filelist'
    file_list = []
    
    results_file = 'evaluation_results.txt'
    
    with open(file_list_path) as f:
        for line in f:
            file_list.append(line.replace('\n',''))
    
    predict_period = 14
    #reg = linear_model.BayesianRidge()

    pdq_terms=[[1,0,0], #AR model
               [2,0,0],
               [0,0,1],               
               [1,0,1], #ARMA model
               [0,1,0],
               [1,1,1]  #ARIMA(1,1,1) model
               ] 

    result={}
    for s in file_list:
        s_data = np.loadtxt(data_path+s,delimiter=',')
        s_y = s_data[:,1]
        s_y_size = s_y.shape[0]
        result[s]=[]
        for term in pdq_terms:
                yhat,MSE,aic = ARIMA_model(s_y,term[0],term[1],term[2])
                result[s].append((MSE,aic))
    
    with open(results_file,mode="w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",",quotechar="'")
        for s in result:
            writer.writerow([s,result[s]])
    
# =============================================================================
#     print('ARIMA model (p,d,q)')
#     for s in result:
#         i=0
#         print(s)
#         for model in result[s]:
#             print('(%s,%s,%s): %.3f(MSE) %.3f(aic)' %(pdq_terms[i][0],
#                   pdq_terms[i][1],pdq_terms[i][2],model[0],model[1]))
#             i=i+1
# =============================================================================

