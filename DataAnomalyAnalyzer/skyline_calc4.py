# coding: utf-8
'''
Created on 2018年4月11日

@author: zhao-PC
利用斜率判断异动
'''

import DataAnomalyAnalyzer.load_data as ld
from DataAnomalyAnalyzer import skyline_algorithms
#import time
import numpy as np
import matplotlib.pyplot as plt
#from DataAnomalyAnalyzer import LinearRegression
from DataAnomalyAnalyzer import tsd_gradient
from sklearn import preprocessing

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
                
        starttime = 1522598400
        endtime = starttime + 60 * 60 * 24
        
        #数据集
        data_value = []
        data_time = []
        
        #异动坐标 
        data_ano_x = []
        data_ano_y = []
        
        #斜率数据集
        data_gradient = []
        #data_coef = []
        
        #斜率异动坐标
        data_xielv_ano_x = []
        data_xielv_ano_y = []
        
        
        for i in range(starttime,endtime - 60,60):
            
            data_value.append(data_dict[i])
            data_time.append(float((i-starttime))/3600)
            
            tmpdata = []
            tmpvalue = []
            
            j=i
            
            for j in range(i,i + 60 * 60,60):
                tmpdata.append((j,data_dict[j]))
                tmpvalue.append(data_dict[j])
        
            anomalous, ensemble, datatime, datapoint = skyline_algorithms.run_selected_algorithm(tmpdata, 'test')

            #time_local = time.localtime(datatime)
                    
            #coef,intercept = LinearRegression.LinearRegression(tmpdata)
            #data_coef.append(coef)
            
            v_gradient = tsd_gradient.getGradient(tmpdata)
            data_gradient.append(v_gradient)

            np_data = np.array(data_gradient)

            min_max_scaler = preprocessing.MinMaxScaler()
            data_xielv_new = min_max_scaler.fit_transform(np_data.reshape(-1, 1))
                        
            #print(v_xielv_mean)
                        
            if anomalous:
                data_ano_x.append(float((datatime-starttime))/3600)
                data_ano_y.append(datapoint)
                
                if data_xielv_new[-1] < 0.3 or data_xielv_new[-1] > 0.7:

                    data_xielv_ano_x.append(float((datatime-starttime))/3600)
                    data_xielv_ano_y.append(datapoint)                                                      

        plt.subplot(3,1,1)
        plt.plot(data_time,data_value,linewidth=0.5)
        
        plt.scatter(data_ano_x,data_ano_y,color='green',s=5)
        plt.scatter(data_xielv_ano_x,data_xielv_ano_y,color='red',s=5)
        
        plt.ylabel('异动判断')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
        
        '''
        plt.subplot(3,1,2)
        
        plt.ylabel('通过线性回归计算的斜率')        
        
        plt.plot(data_time,data_coef,linewidth=0.5)
                
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
        '''
        
        plt.subplot(3,1,3)
        
        plt.ylabel('通过首末点计算的斜率')        
        
        plt.plot(data_time,data_xielv_new,linewidth=0.5)
                
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks) 
        
        plt.show()       