# coding: utf-8
'''
Created on 2018年4月11日

@author: zhao-PC
利用前十天相同时间点数据过滤异动
'''

import DataAnomalyAnalyzer.load_data as ld
from DataAnomalyAnalyzer import skyline_algorithms, tsd_his_gradient,tsd_linear_regression,\
    tsd_gradient, tsd_scaler, tsd_gradient_recent
import time
import numpy as np
import matplotlib.pyplot as plt

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


plt.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

class skyline_calc():
    def calc(self):
        load = ld.load_data()
        
        data = load.csv('busi_yyt.csv')
        
        data_dict = dict(data)
                
        starttime = 1522166400
        endtime = starttime + 60 * 60 * 24
        
        data_value = []
        data_time = []
           
        data_ano_x = []
        data_ano_y = []
        
        data_coef = []
        coef_time = []
        
        data_ano_x_new = []
        data_ano_y_new = []
        
        data_gradient = []      
        
        for i in range(starttime + 60 * 60,endtime,60):
            data_value.append(data_dict[i])
            data_time.append(float((i-starttime))/3600)
            
            tmpdata = []
            tmpvalue = []
            
            for j in range(i - 60 * 60,i,60):
                tmpdata.append((j,data_dict[j]))
                tmpvalue.append(data_dict[j])
        
            anomalous, ensemble, datatime, datapoint = skyline_algorithms.run_selected_algorithm(tmpdata, 'test')

            coef,intercept = tsd_his_gradient.getGradient(datatime, data_dict)
            gradient = tsd_gradient_recent.getGradientRecent(tmpdata)
            
            print('coef:'+str(coef))
            print('gradient:'+str(gradient))
            
                        
            if anomalous:
                data_ano_x.append(float((datatime-starttime))/3600)
                data_ano_y.append(datapoint)
                
                if abs(gradient) > abs(coef) * 1.3 or abs(gradient) < abs(coef) * 0.7:
                    data_ano_x_new.append(float((datatime-starttime))/3600)
                    data_ano_y_new.append(datapoint)
                        
            data_coef.append(coef)
            
            data_gradient.append(gradient)

        '''
        data_coef_new = tsd_scaler.getScaler(data_coef)
        data_gradient_new = tsd_scaler.getScaler(data_gradient)
        

        coef_dict = dict(zip(data_time,data_coef_new))
        gradient_dict = dict(zip(data_time,data_gradient_new))  
        
        for x in data_time:
            if coef_dict[x] >= 0.7 or coef_dict[x] <= 0.3:
                if
                data_ano_x_new.append(x)
                data_ano_y_new.append(data_dict[starttime + x[0] * 3600])
        '''
        #####

        plt.subplot(3,1,1)
        plt.plot(data_time,data_value,linewidth=0.5)
        
        plt.scatter(data_ano_x,data_ano_y,color='green',s=5)
        #plt.scatter(data_ano_x_new,data_ano_y_new,color='red',s=5)        
        
        plt.ylabel('异动判断')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
        
        #####

        plt.subplot(3,1,2)
        plt.plot(data_time,data_coef,linewidth=0.5)
        
        plt.ylabel('前一日斜率')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
        
        #####
        
        plt.subplot(3,1,3)
        plt.plot(data_time,data_gradient,linewidth=0.5)
        
        plt.ylabel('当前斜率')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)             

        plt.show()       