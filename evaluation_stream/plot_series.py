# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 18:41:33 2018

@author: dchow
"""

from pandas.plotting import autocorrelation_plot
from matplotlib import pyplot as plt
import csv

def plot_AC(filename):

    yseries = []
    with open(filename,mode="r",newline='',encoding="utf-8") as csv_file: #read file:KG
        csv_reader = csv.reader(csv_file,delimiter=",",quotechar="'")
        for row in csv_reader:
            if row:
                yseries.append(float(row[1]))
                
    autocorrelation_plot(yseries)

if __name__ =='__main__':
    
    files = []
    
    with open("filelist",mode="r",newline='',encoding="utf-8") as csv_file:
        csv_reader1 = csv.reader(csv_file,delimiter=",",quotechar="'")
        for file in csv_reader1:
            if file:
                plot_AC(file[0])
    plt.show()
# =============================================================================
#     plt.plot(yseries)
#     plt.show()
# =============================================================================

