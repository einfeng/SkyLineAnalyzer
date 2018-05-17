# coding: utf-8

#import DataAnomalyAnalyzer.load_data as ld
import numpy as np
from sklearn import preprocessing

def getEm(data1,data2):

#load = ld.load_data()

#data1 = load.csv('busi_yyt4.csv')
#data2 = load.csv('busi_yyta.csv')

    np_data1 = np.array(data1[19:])
    np_data2 = np.array(data2[19:])
    
    min_max_scaler = preprocessing.MinMaxScaler()
    
    tmpdata_minmax1 = min_max_scaler.fit_transform(np_data1)
    tmpdata_minmax2 = min_max_scaler.fit_transform(np_data2)
    
    s = np.linalg.norm(tmpdata_minmax2 - tmpdata_minmax1)
    
    return s