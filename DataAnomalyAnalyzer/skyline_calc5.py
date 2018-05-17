# coding: utf-8
'''
Created on 2018年4月11日

@author: zhao-PC
利用前十天相同时间点数据过滤异动
'''

import DataAnomalyAnalyzer.load_data as ld
from DataAnomalyAnalyzer import skyline_algorithms
import time
import numpy as np
import matplotlib.pyplot as plt
from DataAnfrom DataAnomalyAnalyzer import tsd_linear_regressionsys
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
        
        data_up = []
        data_down = []
        
        
        for i in range(starttime,endtime,60):
            data_value.append(data_dict[i])
            data_time.append(float((i-starttime))/3600)
            
            tmpdata = []
            tmpvalue = []
            
            j=i
            
            for j in range(i,i + 60 * 29,60):
                tmpdata.append((j,data_dict[j]))
                tmpvalue.append(data_dict[j])
        
            anomalous, ensemble, datatime, datapoint = skyline_algorithms.run_selected_algorithm(tmpdata, 'test')

            time_local = time.localtime(datatime)

            v_mean = 0
            for t in range(1,10):
                v_mean += data_dict[tmpdata[-1][0] - 86400 * t]
                #print(str(datatime) + ':' +str(data_dict[tmpdata[-1][0] - 86400 * t]))
            
            v_mean = v_mean/10
            
            data_up.append(v_mean * 1.3)
            data_down.append(v_mean * 0.7)            
                        
            if anomalous:
                data_ano_x.append(float((datatime-starttime))/3600)
                data_ano_y.append(datapoint)

        plt.subplot(3,1,1)
        plt.plot(data_time,data_value,linewidth=0.5)
        plt.plot(data_time,data_up,linewidth=0.5)
        plt.plot(data_time,data_down,linewidth=0.5)
        
        
        plt.scatter(data_ano_x,data_ano_y,color='green',s=5)
        
        plt.ylabel('异动判断')
        
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
        
        plt.show()       