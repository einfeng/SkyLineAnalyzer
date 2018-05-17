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
from sqlalchemy.sql.expression import false
from pip._vendor.distlib._backport.tarfile import TUREAD
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
        
        datamean = np.mean(data_dict.values())
        
                
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
        
        meandata_list = []
        risedata_list = []        
        
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

            meandata = []

            for j in range(i - 10 * 60,i,60):
                meandata.append(data_dict[j])              

            meandata_list.append(np.mean(meandata))
            
            if len(meandata_list)>1:
                risedata_list.append(meandata_list[-1] - meandata_list[-2])
            else:
                risedata_list.append(0)
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
        plt.plot(data_time,meandata_list,linewidth=0.5)
        
        plt.ylabel('滑动平均数')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
        
        #####

        plt.subplot(3,1,3)
        plt.plot(data_time,risedata_list,linewidth=0.5)
        
        plt.ylabel('增长')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)             

        plt.show()
        
def rise_estimate(data,data_mean):
    rise_rate_threshold = 0
    rise_count_threshold = 50
    
    data_tmp = []
    
    for d in data:
        rate_tmp = 
    
    
    