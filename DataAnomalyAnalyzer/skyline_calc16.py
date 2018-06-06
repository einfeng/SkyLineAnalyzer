# coding: utf-8
'''
Created on 2018年4月11日

@author: zhao-PC
利用前十天相同时间点数据过滤异动
'''

import DataAnomalyAnalyzer.load_data as ld
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from DataAnomalyAnalyzer import tsd_linear_regression
from sklearn import linear_model
from bokeh.layouts import column

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

plt.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# grubbs
# first_hour_average
# least_squares
# histogram_bins
# ks_test


class skyline_calc():

    def calc(self):
        
        busi_data = pd.read_csv('data/busi_yyt.csv', header=None, names=('time', 'value'), parse_dates=['time'], date_parser=(lambda x: pd.datetime.strptime(x, 'yyyy-mm-dd hh24:mi')))
        
        print(busi_data)

        print('xxxxxxxx')
        
        '''
        data_dict = dict(data)        
                
        starttime = 1520611200
        endtime = starttime + 60 * 60 * 24
                
        data_value = []
        data_time = []
        
        data_mv_value = []
        data_mv_time = []
                   
        data1_ano_x = []
        data1_ano_y = []
        
        for i in range(starttime + 30 * 60, endtime, 60):
            
            data_value.append(data_dict[i])
            data_time.append(float((i - starttime)) / 3600)
            
            tmpdata = []
            tmpvalue = []
            
            for j in range(i - 30 * 60, i + 60, 60):
                tmpdata.append((j, data_dict[j]))
                tmpvalue.append(data_dict[j])
                
            
                
            anomalous,pre_value = linearregression(tmpdata,500,'','')
            
            data_mv_time.append(float((i - starttime)) / 3600)
            data_mv_value.append(pre_value)

            if anomalous:
                data1_ano_x.append(float((i - starttime)) / 3600)
                data1_ano_y.append(data_dict[i])                
                
                
                

    
                
                
        #####
        


        plt.subplot(3, 1, 1)
        plt.plot(data_time, data_value, linewidth=0.5)
        plt.plot(data_mv_time, data_mv_value, linewidth=0.5)        
        
        #plt.scatter(data1_ano_x, data1_ano_y, color='green', s=5)
        plt.scatter(data1_ano_x, data1_ano_y, color='red', s=5)

        plt.ylabel('营业厅-3月10日')
        
        my_x_ticks = np.arange(0, 24, 1)
        plt.xticks(my_x_ticks)
     
        plt.show()
        
def linearregression(timeseries,offset_value,work_path, kpi_name,threshold_up=1.3,threshold_down=0.7):
    #利用线性回归判断异动
    np_data = np.array(timeseries[0:len(timeseries)-1])
    
    x = np_data[:, 0]
    y = np_data[:, 1]
        
    linreg = linear_model.LinearRegression()
    linreg.fit(x.reshape(-1, 1), y)
    
    intercept = linreg.intercept_
    coef = linreg.coef_    
                
    calc_value = coef * timeseries[-1][0] + intercept
    
    if timeseries[-1][1] + offset_value < (calc_value + offset_value) * threshold_down or timeseries[-1][1] + offset_value > (calc_value + offset_value) * threshold_up:
        return True,calc_value
    else:
        return False,calc_value
    
'''
