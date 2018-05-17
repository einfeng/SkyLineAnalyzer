# coding: utf-8
'''
Created on 2018年4月11日

@author: zhao-PC
'''
import DataAnomalyAnalyzer.load_data as ld
from DataAnomalyAnalyzer import skyline_algorithms
from DataAnomalyAnalyzer import tsd_euclidean_metric
from time import time
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression


class skyline_calc():
    def calc(self):
        load = ld.load_data()
        
        data = load.csv('busi_yyt.csv')
        
        dict_data = dict(data)
                
        starttime = 1522080000
        endtime = 1523030340
                                        
        for i in range(starttime,endtime,60):
            tmptime = []
            tmpdata = []
            tmpvalue = []
            
            j=i
            for j in range(i,i + 60 * 29,60):
                tmpdata.append((j,dict_data[j]))
                tmptime.append(j)
                tmpvalue.append(dict_data[j])
                                
            anomalous, ensemble, datatime, datapoint = skyline_algorithms.run_selected_algorithm(tmpdata, 'test')
                        
            time_local = time.localtime(datatime)

            if anomalous == True:

                data1 = []
                data2 = []
                data3 = []
                
                data_new = []
                
                '''
                for t in tmptime:
                    data1.append((t - 86400 * 1,dict_data[t - 86400 * 1]))
                    data2.append((t - 86400 * 2,dict_data[t - 86400 * 2]))
                    data3.append((t - 86400 * 3,dict_data[t - 86400 * 3]))
                    data_new.append((t - 86400 * 1,(dict_data[t - 86400 * 1] + dict_data[t - 86400 * 2] + dict_data[t - 86400 * 1])/3))
                
                e1 = euctsd_euclidean_metrictE(data1,data2)
                e2 = euctsd_euclidean_metrictE(data2,data3)
                e3 = euctsd_euclidean_metrictE(data1,data3)
                '''
                 
                v_mean = 0 
                for t in range(1,10):
                    v_mean += dict_data[tmpdata[-1][0] - 86400 * t]
                
                v_mean = v_mean/10 
                print(v_mean)
                if tmpdata[-1][1] < v_mean * 0.7:            
                    print(str(ensemble) + ':' + str(time.strftime("%Y-%m-%d %H:%M:%S",time_local)) + ':' +str(datapoint))
                '''
                print(str(ensemble) + ':' + str(time.strftime("%Y-%m-%d %H:%M:%S",time_local)) + ':' +str(datapoint))
                '''               