# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 22:01:36 2018

@author: dchow
"""
import csv

if __name__ =='__main__':
    """
    Extract feature space (business) from gasStation.txt (KG)
    """
    feature_matrix={}
    feature_list=[]
    header = 0
    with open("KG_bus.txt",mode="r",newline='',encoding="utf-8") as csv_file: #read file:KG
        csv_reader = csv.reader(csv_file,delimiter=",",quotechar="'")
        for row in csv_reader:
            if header == 0: #skip header
                header = header + 1
            elif row:
                if row[0] not in feature_matrix:
                    feature_matrix[row[0]] = []
                if (row[2] + " " + row[1]) not in feature_list:
                    feature_list.append(row[2]+" "+row[1])    

    feature_list.sort()

    for subject in feature_matrix: #initialise feature matrix
        feature_matrix[subject] = [0]*len(feature_list)
        
    header = 0
    with open("KG_bus.txt",mode="r",newline='',encoding="utf-8") as csv_file: #read file:KG
        csv_reader = csv.reader(csv_file,delimiter=",",quotechar="'")
        for row in csv_reader:
            if header == 0: #skip header
                header = header + 1
            elif row:
                feature_num = feature_list.index(row[2]+" "+row[1]) #find feature number
                feature_matrix[row[0]].pop(feature_num)             #remove zero from feature
                feature_matrix[row[0]].insert(feature_num,1)        #add one to feature


    with open('fs_bus',mode='w',encoding='utf-8') as output_file: #write file: feature space
        for feature in feature_list:
            output_file.write(str(feature)+'\n')
    output_file.closed
    
    with open('fm_bus', 'w',encoding='utf-8') as output_file: #write file: feature matrix
        for subject in feature_matrix:
            output_file.write(str(subject))
            for val in feature_matrix[subject]:
                output_file.write(','+str(val))
            output_file.write('\n')
    output_file.closed

#    with open('evaluation_results', "w") as output_file:
#        for lag in range(2,11):
#            output_file.write(str(lag))
#            for t_ahead in range (1,15):
#                output_file.write(',' + str(MSE[lag-2,t_ahead-1]))
#            output_file.write('\n')
#    output_file.closed
