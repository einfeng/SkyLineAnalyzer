# coding: utf-8
'''
Created on 2018年4月11日

@author: zhao-PC
利用前十天相同时间点数据过滤异动
'''

import DataAnomalyAnalyzer.load_data as ld
import numpy as np
import matplotlib.pyplot as plt
import sys
from DataAnomalyAnalyzer.skyline_algorithms import run_selected_algorithm
import pandas as pd
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
        
        data = load.csv('busi_yyt.csv')
        
        data_dict = dict(data)        
                
        starttime = 1522166400
        endtime = starttime + 60 * 60 * 24
        
        starttime1 = starttime - 60 * 60 * 24 * 1
        endtime1 = endtime - 60 * 60 * 24 * 1
        
        starttime2 = starttime - 60 * 60 * 24 * 2
        endtime2 = endtime - 60 * 60 * 24 * 2
        
        starttime3 = starttime - 60 * 60 * 24 * 3
        endtime3 = endtime - 60 * 60 * 24 * 3      
        
        starttime4 = starttime - 60 * 60 * 24 * 4
        endtime4 = endtime - 60 * 60 * 24 * 4     
        
        starttime5 = starttime - 60 * 60 * 24 * 5
        endtime5 = endtime - 60 * 60 * 24 * 5                  
        
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []                        
        
        for i in range(starttime1,endtime1,60):
            data1.append((i,data_dict[i]))
            
        for i in range(starttime2,endtime2,60):
            data2.append((i,data_dict[i]))
            
        for i in range(starttime3,endtime3,60):
            data3.append((i,data_dict[i]))
            
        for i in range(starttime4,endtime4,60):
            data4.append((i,data_dict[i]))
            
        for i in range(starttime5,endtime5,60):
            data5.append((i,data_dict[i]))                                    
            
        data_list = [data1,data2]
                
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
                
            anomalous,mv_value = history_movingaverage(tmpdata,data_list)
                
            #anomalous, ensemble, datatime, datapoint = run_selected_algorithm(tmpdata,'test')
                        
            data_mv_value.append(mv_value)
            data_mv_time.append(float((i - starttime)) / 3600)
            
            if anomalous:
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
        


        plt.subplot(3, 1, 1)
        plt.plot(data_time, data_value, linewidth=0.5)
        plt.plot(data_mv_time, data_mv_value, linewidth=0.5)        
        
        #plt.scatter(data1_ano_x, data1_ano_y, color='green', s=5)
        #plt.scatter(data1_ano_x, data1_ano_y, color='red', s=5)

        plt.ylabel('4月1日-处理前')
        
        my_x_ticks = np.arange(0, 24, 1)
        plt.xticks(my_x_ticks)
     
        plt.show()
        
        
def history_movingaverage(timeseries,his_timeseries_list):
    
    ts = pd.DataFrame(timeseries)
    ts_len = len(ts)
    
    data_time = ts.iloc[-1][0]
    data_value = ts.iloc[-1][1]
    data_time_loc = time.localtime(data_time)
    
    print(data_time_loc)
        
    data_hour = data_time_loc[3]
    data_min = data_time_loc[4]
        
    his_value = 0
    his_mean = 0
        
    for his_data in his_timeseries_list:
        his_df = pd.DataFrame(his_data)

        for his_row in his_df.iterrows():
            if time.localtime(his_row[1][0])[3]==data_hour and time.localtime(his_row[1][0])[4]==data_min:
                if his_row[0] < ts_len/2 or his_row[0] >= len(his_df) - ts_len/2:
                #if his_row[0] < 720 or his_row[0] >= len(his_df) - 720:
                    his_value = his_row[1][1]
                    #print(his_row[1][0])
                else:
                    his_value = np.mean(his_df[his_row[0] - ts_len/2:his_row[0] + ts_len/2][1])
                    #print(his_row[1][0])
            
        his_value += his_value
        his_mean += np.mean(his_df[1])
        
    his_value = his_value/len(his_timeseries_list)
    his_mean = his_mean/len(his_timeseries_list)
    
    print(data_value)
    print(his_value)
    print(his_mean)
    '''
    if data_value > his_value + his_value * 0.5 or data_value < his_value - his_value * 0.5:
        return True,his_value
    else:
        return False,his_value
    '''
    
    if data_value/his_mean <= 0.3:
        if data_value >= his_value * 5:
            return True,his_value
        else:
            return False,his_value
    elif data_value/his_mean >0.3 and data_value/his_mean < 1.7:   
        if data_value >= his_value * 1.5 or data_value <= his_value * 0.5:
            return True,his_value
        else:
            return False,his_value
    elif data_value/his_mean >= 1.7:
        if data_value >= his_value * 1.5 or data_value <= his_value * 0.5:
            return True,his_value
        else:
            return False,his_value    