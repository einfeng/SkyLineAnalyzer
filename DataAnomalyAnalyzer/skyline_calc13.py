# coding: utf-8
'''
Created on 2018年4月11日

@author: zhao-PC
利用前十天相同时间点数据过滤异动
'''

import DataAnomalyAnalyzer.load_data as ld
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import t
import sys
from pandas.stats import moments
import time


defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

plt.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

#grubbs
#first_hour_average
#least_squares
#histogram_bins
#ks_test

class skyline_calc():

    def calc(self):
        load = ld.load_data()
        
        data = load.csv('busi_hzs.csv')
        
        data_dict = dict(data)        
                
        starttime = 1522684800
        endtime = starttime + 60 * 60 * 24
        
        data_value = []
        data_time = []
           
        data1_ano_x = []
        data1_ano_y = []
        
        data2_ano_x = []
        data2_ano_y = []
        
        data2_ano_x_line = []
        data2_ano_y_line = []        
        
        data3_ano_x = []
        data3_ano_y = []      
        
        data3_ano_x_line = []
        data3_ano_y_line = []                 
        
        ano_count = 0
        ano_count_new = 0        

        for i in range(starttime + 5 * 60, endtime, 60):
            data_value.append(data_dict[i])
            data_time.append(float((i - starttime)) / 3600)
            
            tmpdata = []
            tmpvalue = []
            
            for j in range(i - 5 * 60, i + 60, 60):
                tmpdata.append((j, data_dict[j]))
                tmpvalue.append(data_dict[j])
                
            data_max = np.max(dict(tmpdata).values())
            data_min = np.min(tmpdata)
            
            print(data_max)             
            
            if data_dict[j] < data_max * 0.5 or data_dict[j] > data_min * 1.5:
                ano_count += 1
                data1_ano_x.append(float((i - starttime)) / 3600)
                data1_ano_y.append(data_dict[i])     
                
                '''
                # 异动点
                if time_local[3] >= 7 and time_local[3] < 23:
                    data_filter = anomaly_filter(i, data)
                    if data_filter:
                        #if upanddown(tmpdata,1):
                            ano_count_new+=1
                            data2_ano_x.append(float((i - starttime)) / 3600)
                            data2_ano_y.append(data_dict[i])
                '''
              


                
                
        #####
        
        print(ano_count)
        print(ano_count_new)

        plt.subplot(3, 1, 1)
        plt.plot(data_time, data_value, linewidth=0.5)
        
        #plt.scatter(data1_ano_x, data1_ano_y, color='green', s=5)
        plt.scatter(data1_ano_x, data1_ano_y, color='red', s=5)

        plt.ylabel('4月1日-处理前')
        
        my_x_ticks = np.arange(0, 24, 1)
        plt.xticks(my_x_ticks)
        
 

        plt.show()


def median_absolute_deviation_new(timeseries):

    current_result = median_absolute_deviation(timeseries)
    result = []
    for i in range(5):
        timeseries = timeseries[0:len(timeseries)-1]
        if median_absolute_deviation(timeseries):
            result.append(True)
        else:
            result.append(False)     
    
    if current_result == True and result.count(True)==0:
        return True
    else:
        return False

        
def median_absolute_deviation(timeseries):
    """
    A timeseries is anomalous if the deviation of its latest datapoint with
    respect to the median is X times larger than the median of deviations.
    """
    # print('算法计算: median_absolute_deviation')

    series = pd.Series([x[1] for x in timeseries])
    median = series.median()
    demedianed = np.abs(series - median)
    median_deviation = demedianed.median()

    # The test statistic is infinite when the median is zero,
    # so it becomes super sensitive. We play it safe and skip when this happens.
    if median_deviation == 0:
        return False

    test_statistic = demedianed.iget(-1) / median_deviation
#     
#     print('median:'+str(median))
#  
#     print('median_deviation:'+str(median_deviation))
#     print('demedianed.iget(-1):'+str(demedianed.iget(-1)))
#     print('test_statistic:'+str(test_statistic))

    # Completely arbitary...triggers if the median deviation is
    # 6 times bigger than the median
    if test_statistic > 6:
        return True
    
def median_absolute_deviation_down(timeseries):

    series = pd.Series([x[1] for x in timeseries])
    median = series.median()
    demedianed = np.abs(series - median)
    median_deviation = demedianed.median()
    
    mean = np.mean(series)

    if median_deviation == 0:
        return False

    test_statistic = demedianed.iget(-1) / median_deviation

    if test_statistic > 6 and series.iget(-1) < mean:
        return True
    else:
        return False
    
def median_absolute_deviation_up(timeseries):

    series = pd.Series([x[1] for x in timeseries])
    median = series.median()
    demedianed = np.abs(series - median)
    median_deviation = demedianed.median()
    
    mean = np.mean(series)

    if median_deviation == 0:
        return False

    test_statistic = demedianed.iget(-1) / median_deviation

    if test_statistic > 6 and series.iget(-1) > mean:
        return True
    else:
        return False    

def timestamp0(timestamp):
    # 功能：计算某一固定时间点的日开始时间
    # 开发人：赵震宇
    # 开发时间：2018年5月8日
    #
    # ####输入参数####
    #
    # ####返回值####
    #
    timestamp0 = timestamp - (timestamp + 86400 * 8 / 24) % 86400
    return timestamp0


def anomaly_filter(anomalytime, datalist, dataperiod=60, mvcyclecount=10,trendcyclecount=30, swingthreshold=0.3, minusthreshold=10):
    # 功能：过滤异动点
    # 开发人：赵震宇
    # 开发时间：2018年5月8日
    #    
    # ####输入参数####
    # anomalytime：异动时间点
    # datalist：数据集（list）
    # period：周期，单位：秒，默认值：60
    # mvcyclecount：滑动平均计算周期数，默认值：10
    # trendcyclecount：趋势判断计算周期数，默认值：30
    # swingthreshold：异动指标瞬时浮动阀值（百分比），默认值：0.3（30%）
    # minusthreshold：异动指标变化趋势判断阀值，默认值：10
    #
    # ####返回值####
    # 返回值1：是否异动。True：异动；Flase：不异动。
    
    datadict = dict(datalist)
    
    # 获取前一天的滑动平均数
    lastday_data = []
    
    lastday_starttime = timestamp0(anomalytime - 86400)
    lastday_endtime = lastday_starttime + 86400 - dataperiod
    
    for j in range(lastday_starttime, lastday_endtime, dataperiod):
        lastday_data_mean = []
        
        for m in range(j - mvcyclecount * dataperiod, j, dataperiod):
            lastday_data_mean.append(datadict[m])
        
        lastday_data.append((j, np.mean(lastday_data_mean)))
    
    lastday_data_dict = dict(lastday_data)
    
    # 获取前一天的平均值
    mean = np.mean(dict(lastday_data).values())
    
    # 获取前一天滑动平均数的变化量
    
    lastday_data_minus = []
    
    for j in range(anomalytime - 86400, anomalytime - 86400 + trendcyclecount * dataperiod, dataperiod):
        lastday_data_minus.append(round(lastday_data_dict[j + dataperiod] - lastday_data_dict[j], 3))
        # print(round(lastday_data_dict[j+60] - lastday_data_dict[j],3)/mean)
    
    # 前一天滑动平均数变化标记。递增为1，递减为-1。
    lastday_data_minus_flag = []
    
    for j in lastday_data_minus:
        if j > 0:
            lastday_data_minus_flag.append(1)
        elif j < 0:
            lastday_data_minus_flag.append(-1)
        else:
            lastday_data_minus_flag.append(0)
        
    # 异动点异动幅度标记。如果异动点的异动幅度超过平均值20%，则判断该异动点有效
    swing_flag = 0
    for j in range(anomalytime - 2 * dataperiod, anomalytime + 2 * dataperiod, dataperiod):
        if abs(datadict[j] - datadict[j - 60]) > swingthreshold * mean:
            swing_flag = 1
    
    # 过滤后的异动点
    if (lastday_data_minus_flag.count(1) > minusthreshold and lastday_data_minus_flag.count(-1) > minusthreshold and swing_flag == 1) or swing_flag == 1:
        return True
    else:
        return False
    
def upanddown(timestamp,flag):
    value=0
    for i in range(1,4,1):
        value += timestamp[-1][1] - timestamp[-i][1]
        
    value = value / 3
    
    if (flag == 0 and value > 0) or ((flag == 1 and value < 0)):
        return True
    else:
        return False
    
    