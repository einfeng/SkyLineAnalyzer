# coding: utf-8
'''
Created on 2018年4月11日

@author: zhao-PC
利用前十天相同时间点数据过滤异动
'''

import DataAnomalyAnalyzer.load_data as ld
from DataAnomalyAnalyzer import skyline_algorithms
import numpy as np
import matplotlib.pyplot as plt
import pandas
import scipy
from scipy.stats import t
import sys
from pandas.stats import moments
from scipy.stats import ks_2samp
import statsmodels.api as sm

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
        
        data = load.csv('busi_yyt.csv')
        
        data_dict = dict(data)        
                
        starttime = 1522080000
        endtime = starttime + 60 * 60 * 24
        
        data_value = []
        data_time = []
           
        data1_ano_x = []
        data1_ano_y = []
        
        data2_ano_x = []
        data2_ano_y = []
        
        data3_ano_x = []
        data3_ano_y = []
        
        data4_ano_x = []
        data4_ano_y = []
             
        
        for i in range(starttime + 60 * 60, endtime, 60):
            data_value.append(data_dict[i])
            data_time.append(float((i - starttime)) / 3600)
            
            tmpdata = []
            tmpvalue = []
            
            for j in range(i - 30 * 60, i, 60):
                tmpdata.append((j, data_dict[j]))
                tmpvalue.append(data_dict[j])

            print(tmpdata[-1])
            print(data_dict[i])
        
            anomalous1 = median_absolute_deviation(tmpdata)
            
            print(anomalous1)
            
            if anomalous1:
                # 异动点
                data1_ano_x.append(float((i - 60 - starttime)) / 3600)
                data1_ano_y.append(data_dict[i-60])
                
            anomalous2 = stddev_from_average(tmpdata)
            
            if anomalous2:
                # 异动点
                data2_ano_x.append(float((i - 60 - starttime)) / 3600)
                data2_ano_y.append(data_dict[i - 60])
                
            anomalous3 = stddev_from_moving_average(tmpdata)
            
            if anomalous3:
                # 异动点
                data3_ano_x.append(float((i - 60 - starttime)) / 3600)
                data3_ano_y.append(data_dict[i - 60])
                
            anomalous4 = mean_subtraction_cumulation(tmpdata)
            
            if anomalous4:
                # 异动点
                data4_ano_x.append(float((i - 60 - starttime)) / 3600)
                data4_ano_y.append(data_dict[i - 60])
                
                
        #####

        plt.subplot(4, 1, 1)
        plt.plot(data_time, data_value, linewidth=0.5)
        
        plt.scatter(data1_ano_x, data1_ano_y, color='green', s=5)

        plt.ylabel('median_absolute_deviation')
        
        my_x_ticks = np.arange(0, 24, 1)
        plt.xticks(my_x_ticks)
        

        
        plt.subplot(4, 1, 2)
        plt.plot(data_time, data_value, linewidth=0.5)
        
        plt.scatter(data2_ano_x, data2_ano_y, color='green', s=5)

        plt.ylabel('stddev_from_average')
        
        my_x_ticks = np.arange(0, 24, 1)
        plt.xticks(my_x_ticks)
        
        plt.subplot(4, 1, 3)
        plt.plot(data_time, data_value, linewidth=0.5)
        
        plt.scatter(data3_ano_x, data3_ano_y, color='green', s=5)

        plt.ylabel('stddev_from_moving_average')
        
        my_x_ticks = np.arange(0, 24, 1)
        plt.xticks(my_x_ticks) 
        
        plt.subplot(4, 1, 4)
        plt.plot(data_time, data_value, linewidth=0.5)
        
        plt.scatter(data4_ano_x, data4_ano_y, color='green', s=5)

        plt.ylabel('mean_subtraction_cumulation')
        
        my_x_ticks = np.arange(0, 24, 1)
        plt.xticks(my_x_ticks)
        

        
        '''  
        #####

        plt.subplot(3,1,2)
        plt.plot(data_time,lastday_data_minus,linewidth=0.5)
        
        plt.ylabel('滑动平均数')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
      
        #####

        plt.subplot(3,1,3)
        plt.plot(data_time,risedata_list,linewidth=0.5)
        
        plt.ylabel('增长')
        
        my_x_ticks = np.arange(0,24,1)
        plt.xticks(my_x_ticks)
        '''            

        plt.show()

def tail_avg(timeseries):
    """
    This is a utility function used to calculate the average of the last three
    datapoints in the series as a measure, instead of just the last datapoint.
    It reduces noise, but it also reduces sensitivity and increases the delay
    to detection.
    """
    try:
        t = (timeseries[-1][1] + timeseries[-2][1] + timeseries[-3][1]) / 3
        return t
    except IndexError:
        return timeseries[-1][1]
        
        
def median_absolute_deviation(timeseries):
    """
    A timeseries is anomalous if the deviation of its latest datapoint with
    respect to the median is X times larger than the median of deviations.
    """
    # print('算法计算: median_absolute_deviation')

    series = pandas.Series([x[1] for x in timeseries])
    median = series.median()
    demedianed = np.abs(series - median)
    median_deviation = demedianed.median()

    # The test statistic is infinite when the median is zero,
    # so it becomes super sensitive. We play it safe and skip when this happens.
    if median_deviation == 0:
        return False

    test_statistic = demedianed.iget(-1) / median_deviation
    
    print('median:'+str(median))

    print('median_deviation:'+str(median_deviation))
    print('demedianed.iget(-1):'+str(demedianed.iget(-1)))
    print('test_statistic:'+str(test_statistic))

    # Completely arbitary...triggers if the median deviation is
    # 6 times bigger than the median
    if test_statistic > 6:
        return True

def stddev_from_average(timeseries):
    """
    A timeseries is anomalous if the absolute value of the average of the latest
    three datapoint minus the moving average is greater than three standard
    deviations of the average. This does not exponentially weight the MA and so
    is better for detecting anomalies with respect to the entire series.
    """
    # print('算法计算: stddev_from_average')    
    
    series = pandas.Series([x[1] for x in timeseries])
    mean = series.mean()
    stdDev = series.std()
    t = tail_avg(timeseries)

    return abs(t - mean) > 2 * stdDev

def stddev_from_moving_average(timeseries):
    """
    A timeseries is anomalous if the absolute value of the average of the latest
    three datapoint minus the moving average is greater than three standard
    deviations of the moving average. This is better for finding anomalies with
    respect to the short term trends.
    """
    # print('算法计算: stddev_from_moving_average')
    
    series = pandas.Series([x[1] for x in timeseries])
    expAverage = moments.ewma(series, com=50)
    stdDev = moments.ewmstd(series, com=50)

    return abs(series.iget(-1) - expAverage.iget(-1)) > 3 * stdDev.iget(-1)

def mean_subtraction_cumulation(timeseries):
    """
    A timeseries is anomalous if the value of the next datapoint in the
    series is farther than three standard deviations out in cumulative terms
    after subtracting the mean from each data point.
    """
    
    # print('算法计算: mean_subtraction_cumulation')

    series = pandas.Series([x[1] if x[1] else 0 for x in timeseries])
    series = series - series[0:len(series) - 1].mean()
    stdDev = series[0:len(series) - 1].std()
    expAverage = moments.ewma(series, com=15)

    return abs(series.iget(-1)) > 3 * stdDev
