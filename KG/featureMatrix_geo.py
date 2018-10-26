# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 13:40:05 2018

@author: dchow
"""

import csv

def add_value(feature_matrix, matrix_key,feature_num,value):
    feature_matrix[matrix_key].pop(feature_num)             #remove entry @ feature_num
    feature_matrix[matrix_key].insert(feature_num,value)    #add value @ feature_num

if __name__ =='__main__':
    """
    Extract feature space (geographic) from KG:
    suburbNSW_set.txt is a KG with suburb related data (e.g. postcode, population)
    2016_08.csv contains service station data from 2016_08
    retail2fuelbrand.txt contains known fuel suppliers at retail brands
    """

    r2fbrand={}
    feature_list=["HAS_POPULATION","HAS_POSTCODE"]
    header = 0
    with open("retail2fuelbrand.txt",mode="r",newline='',encoding="utf-8") as csv_file: #read file:retail to fuel brands
        csv_reader = csv.reader(csv_file,delimiter=",",quotechar="'")
        for row in csv_reader:
            if row:
               r2fbrand[row[0]]=row[1]
               if "FUEL_BRAND " + str(row[1]) not in feature_list:
                   feature_list.append("FUEL_BRAND " + str(row[1]))

    subPop ={}
    with open("KG_geo.txt",mode="r",newline='',encoding="utf-8") as csv_file: #read file:suburb KG
        csv_reader = csv.reader(csv_file,delimiter=",",quotechar="'")
        for row in csv_reader:
            if row and row[2] == "HAS_POPULATION":
                subPop[row[0]] = row[1]
    
    feature_matrix={}
    header=0
    with open("2016_08.csv",mode="r",newline='',encoding="utf-8") as csv_file: #read file:gas station data
        csv_reader = csv.reader(csv_file,delimiter=",",quotechar='"')
        for row in csv_reader:
            if header == 0: #skip header
                header = header + 1
            elif row:
                if row[0] not in feature_matrix:
                    feature_matrix[row[0]] = []
                if ("RETAIL_BRAND " + row[4]) not in feature_list:
                    feature_list.append("RETAIL_BRAND " + str(row[4]))
                if ("HAS_FUEL_TYPE " + str(row[5])) not in feature_list:
                    feature_list.append("HAS_FUEL_TYPE " + str(row[5]))

    feature_list.sort()

    for subject in feature_matrix: #initialise feature matrix
        feature_matrix[subject] = [0]*len(feature_list)
    
    feature_num_pop = feature_list.index("HAS_POPULATION")
    feature_num_post = feature_list.index("HAS_POSTCODE")
    header = 0
    with open("2016_08.csv",mode="r",newline='',encoding="utf-8") as csv_file: #read file:gas station data
        csv_reader = csv.reader(csv_file,delimiter=",",quotechar='"')
        for row in csv_reader:
            if header == 0: #skip header
                header = header + 1
            elif row:
                if feature_matrix[row[0]][feature_num_pop] == 0:
                    feature_matrix[row[0]].pop(feature_num_pop)
                    if subPop.get(row[2]) != None:
                        feature_matrix[row[0]].insert(feature_num_pop,subPop[row[2]])
                    else:
                        feature_matrix[row[0]].insert(feature_num_pop,-1)

                if feature_matrix[row[0]][feature_num_post] == 0:
                    feature_matrix[row[0]].pop(feature_num_post)
                    feature_matrix[row[0]].insert(feature_num_post,row[3])
                

                feature_num = feature_list.index("HAS_FUEL_TYPE " + row[5])
                if feature_matrix[row[0]][feature_num] == 0:
                    feature_matrix[row[0]].pop(feature_num)             #remove zero from feature
                    feature_matrix[row[0]].insert(feature_num,1)        #add one to feature
                
                feature_num = feature_list.index("RETAIL_BRAND " + row[4])
                if feature_matrix[row[0]][feature_num] == 0:
                    feature_matrix[row[0]].pop(feature_num)             #remove zero from feature
                    feature_matrix[row[0]].insert(feature_num,1)
                    fuel_brand = r2fbrand[row[4]]
                    feature_num_fuel = feature_list.index("FUEL_BRAND " + fuel_brand)
                    feature_matrix[row[0]].pop(feature_num_fuel)             #remove zero from feature
                    feature_matrix[row[0]].insert(feature_num_fuel,1)

    with open("fs_geo",mode="w", encoding="utf-8") as csv_file: #write file: feature space
        writer = csv.writer(csv_file, delimiter=",",quotechar="'")
        for feature in feature_list:
            writer.writerow([feature])

    with open("fm_geo",mode="w", encoding="utf-8") as output_file: #write file: feature matrix
        for subject in feature_matrix:
            output_file.write(str(subject))
            for val in feature_matrix[subject]:
                output_file.write(','+str(val))
            output_file.write('\n')
    output_file.closed