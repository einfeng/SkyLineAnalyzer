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

      
            if anomalous:
                data_ano_x.append(float((datatime-starttime))/3600)
                data_ano_y.append(datapoint)
                
                data_ano_point = (float((datatime-starttime))/3600,datapoint)
                
                tmptime = datatime - 86400
                
                tmpdata_front = []
                tmpdata_back = []
                
                
                for i in range(1,6,1):
                    tmpdata_front.append((tmptime + i * 5 * 60,data_dict[tmptime + i * 5 * 60]))
                    tmpdata_back.append((tmptime - i * 5 * 60,data_dict[tmptime - i * 5 * 60]))
                    
                print(tmpdata_front)
                print(tmpdata_back)

                result_front = isgradiented(data_ano_point,tmpdata_front,datamean,'front')
                result_back = isgradiented(data_ano_point,tmpdata_back,datamean,'back') 
                
                print('front:'+str(result_front))
                print('back:'+str(result_back))          

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
        
def isgradiented(datapoint,datalist,datamean,datatype):
    
    rise_list1 = []
    rise_list2 = []
    rise_list2_tmp = []  
    
    if datatype=='front':
        for i in range(1,5,1):

            rise = datalist[i][1] - datalist[i-1][1]
            
            print(rise)            
            
            if rise >= 0:
                rise_list1.append(1)
            else:
                rise_list1.append(-1)
                
            rise_list2.append(abs(rise))
    elif datatype=='back':
        for i in range(1,5,1):

            rise = datalist[-i-1][1] - datalist[-i][1]
            
            print(rise)
            
            if rise >= 0:
                rise_list1.append(1)
            else:
                rise_list1.append(-1)
                
            rise_list2.append(abs(rise))
    else:
        return None
    ''' 
                    
    print(rise_list2)
             
    for i in rise_list2:
   
        if i/datamean > 0.1:
            rise_list2_tmp.append(1)
        else:
            rise_list2_tmp.append(-1)
    
    if rise_list2_tmp.count(1) == 5:
        if rise_list1[0] == 1:
            if rise_list1.count(1) == 5:
                return True
            else:
                return False
        else:
            if rise_list1.count(-1) == 5:
                return True
            else:
                return False
    else:
        return False
    '''    