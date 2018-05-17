# coding: utf-8
'''
Created on 2018年5月3日

@author: zhao-PC
'''

import tsd_linear_regression

def getGradient(datatime,data_dict):
    
    tmptime = datatime - 86400
    tmpdata_lastday = []
    
    for j in range(tmptime,tmptime + 60 * 60,60):
        tmpdata_lastday.append((j,data_dict[j]))          
    
    coef,intercept = tsd_linear_regression.getLinearRegression(tmpdata_lastday)
    
    return coef,intercept
    