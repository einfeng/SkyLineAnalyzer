# coding: utf-8
'''
Created on 2018年4月11日

@author: zhao-PC
'''
import DataAnomalyAnalyzer.load_data as ld
from DataAnomalyAnalyzer import skyline_algorithms
import time


class skyline_calc():
    def calc(self):
        load = ld.load_data()
        
        data = []
        
        load = load.csv('busi_1.csv')
        
        for key in sorted(load):
            data.append((key,load[key]))
        
        cnt = data.__len__()
                
        i = 0
        while i <= data.__len__() - 60:
            tmpdata = []
            j=i
            while j<i+60:
                tmpdata.append(data[j])
                j += 1
                
            anomalous, ensemble, datatime, datapoint = skyline_algorithms.run_selected_algorithm(tmpdata, 'test')
            
            '''
            if anomalous:
                
                time_local = time.localtime(datatime)
                
                print(str(ensemble) + ':' + str(time.strftime("%Y-%m-%d %H:%M:%S",time_local)) + ':' +str(datapoint))
            '''
            
            time_local = time.localtime(datatime)
            
            print(str(ensemble) + ':' + str(time.strftime("%Y-%m-%d %H:%M:%S",time_local)) + ':' +str(datapoint))

            
            i += 1
            
        