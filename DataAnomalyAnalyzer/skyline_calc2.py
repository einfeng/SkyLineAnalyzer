# coding: utf-8
'''
Created on 2018年4月11日

@author: zhao-PC
'''
import DataAnomalyAnalyzer.load_data as ld
from DataAnomalyAnalyzer import skyline_algorithms
import time
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression


class skyline_calc():
    def calc(self):
        load = ld.load_data()
        
        data = load.csv('busi_yyt.csv')
        
        for i in range(data.__len__() - 30):
            tmpdata = []
            j=i
            
            for j in range(i+30):
                tmpdata.append(data[j])
                                
            anomalous, ensemble, datatime, datapoint = skyline_algorithms.run_selected_algorithm(tmpdata, 'test')
            
            time_local = time.localtime(datatime)

            #if time_local[3] >= 9 and time_local[3] < 18 and anomalous == True:
                                
            #    print(str(ensemble) + ':' + str(time.strftime("%Y-%m-%d %H:%M:%S",time_local)) + ':' +str(datapoint))

            print(str(ensemble) + ':' + str(time.strftime("%Y-%m-%d %H:%M:%S",time_local)) + ':' +str(datapoint))
            
        