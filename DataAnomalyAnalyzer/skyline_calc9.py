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
                
        starttime = 1522252800
        endtime = starttime + 60 * 60 * 24
        
        data_value = []
        data_time = []
           
        data_ano_x = []
        data_ano_y = []
        
        data_ano_x_new = []
        data_ano_y_new = []

        data1 = []
        
        lastday_data_dict = {}
        
        
        for i in range(starttime + 60 * 60,endtime,60):
            data_value.append(data_dict[i])
            data_time.append(float((i-starttime))/3600)
            
            tmpdata = []
            tmpvalue = []
            
            for j in range(i - 30 * 60,i,60):
                tmpdata.append((j,data_dict[j]))
                tmpvalue.append(data_dict[j])
        
            anomalous, ensemble, datatime, datapoint = skyline_algorithms.run_selected_algorithm(tmpdata, 'test')

            if anomalous:
                
                #异动点
                data_ano_x.append(float((i-starttime))/3600)
                data_ano_y.append(datapoint)

                #获取前一天的滑动平均数
                lastday_data = []
                
                lastday_starttime = timestamp0(datatime - 86400)
                lastday_endtime = lastday_starttime + 86400 - 60
                
                for j in range(lastday_starttime,lastday_endtime,60):
                    lastday_data_mean = []
                    
                    for m in range(j - 10 * 60,j,60):
                        lastday_data_mean.append(data_dict[m])
                    
                    lastday_data.append((j,np.mean(lastday_data_mean)))
                
                lastday_data_dict = dict(lastday_data)
                                        
                #获取前一天的平均值
                mean = np.mean(dict(lastday_data).values())
                
                #获取前一天滑动平均数的变化量
                
                lastday_data_minus = []
                
                for j in range(datatime - 86400,datatime - 86400 + 30 * 60, 60):
                    lastday_data_minus.append(round(lastday_data_dict[j+60] - lastday_data_dict[j],3))
                    #print(round(lastday_data_dict[j+60] - lastday_data_dict[j],3)/mean)
                
                #前一天滑动平均数变化标记。递增为1，递减为-1。
                lastday_data_minus_flag = []
                
                for j in lastday_data_minus:
                    if j > 0:
                        lastday_data_minus_flag.append(1)
                    elif j < 0:
                        lastday_data_minus_flag.append(-1)
                    else:
                        lastday_data_minus_flag.append(0)
                        
                #print('上升：'+str(lastday_data_minus_flag.count(1)))
                #print('下降：'+str(lastday_data_minus_flag.count(-1)))   
                #print('0：'+str(lastday_data_minus_flag.count(0)))
                #print('xxx:'+str((data_dict[i] - data_dict[i-60])/mean))
                
                #swing = data_dict[i] - data_dict[i - 60]
                
                #异动点异动幅度标记。如果异动点的异动幅度超过平均值20%，则判断该异动点有效
                swing_flag = 0
                for j in range(i - 2 * 60,i + 2 * 60,60):
                    if abs(data_dict[j] - data_dict[j - 60]) > 0.3 * mean:
                        swing_flag = 1
                
                #异动点历史趋势判断
                minus_count = 10
                
                #过滤后的异动点
                if (lastday_data_minus_flag.count(1) > minus_count and lastday_data_minus_flag.count(-1) > minus_count and swing_flag == 1) or swing_flag == 1:
                    
                    #如果异动点的异动幅度超过平均值20%，则判断该异动点有效
                    data_ano_x_new.append(float((i-starttime))/3600)
                    data_ano_y_new.append(datapoint)
                
        #####
        
        for i in data_time:
            data1.append(lastday_data_dict[int(i * 3600 + starttime - 86400 - 60)])

        print('总异动点数：'+str(data_ano_y.__len__()))
        print('过滤后异动点数：'+str(data_ano_y_new.__len__()))        

        plt.subplot(3,1,1)
        plt.plot(data_time,data_value,linewidth=0.5)
        
        plt.scatter(data_ano_x,data_ano_y,color='green',s=5)
        plt.scatter(data_ano_x_new,data_ano_y_new,color='red',s=5)        

        plt.ylabel('异动判断')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
        
 
        #####

        plt.subplot(3,1,2)
        plt.plot(data_time,data1,linewidth=0.5)
        
        plt.ylabel('滑动平均数')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
        '''       
        #####

        plt.subplot(3,1,3)
        plt.plot(data_time,risedata_list,linewidth=0.5)
        
        plt.ylabel('增长')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
        '''            

        plt.show()
    

    
def timestamp0(timestamp):
    timestamp0 = timestamp-(timestamp + 86400 * 8 / 24)%86400
    return timestamp0

    