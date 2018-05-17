# coding: utf-8
'''
Created on 2018年4月9日

@author: zhao-PC
'''

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import DataAnomalyAnalyzer.load_data as ld

#from sklearn import svm
#from sklearn.covariance import EllipticEnvelope
#from sklearn.ensemble import IsolationForest
#from sklearn.neighbors import LocalOutlierFactor


class isolation_forest():

    def IsolationForest(self):
                
        load = ld.load_data()
        
        data1 = load.csv('busi_qd.csv')
        
        data1_new = []
        data2_new = []

        for d in data1:
            data1_new.append(d[0])
            
        for d in data1:
            data2_new.append(d[1])            

        '''
        datakey = {}
        
        index = 0
        
        for key in data1.keys():
            
            tmplist = []
            
            if data1.has_key(key):
                tmplist.append(float(data1.get(key)))
            else:
                tmplist.append(None)
                
            if data2.has_key(key):
                tmplist.append(float(data2.get(key)))
            else:
                tmplist.append(None)
                
            if data3.has_key(key):
                tmplist.append(float(data3.get(key)))
            else:
                tmplist.append(None)
                
            data.append(tmplist)
            
            index += 1
            
            datakey[index] = key
            
        '''
        
        data = zip(data1_new,data2_new)
        
        
        array = np.array(data)         
        
        clf = IsolationForest() #contamination=0.9
        clf.fit(array)
        y_pred_train = clf.predict(array)
        
        anomaly_point_x = []
        anomaly_point_y = []
        #anomaly_point_z = []
        normal_point_x = []
        normal_point_y = []
        #normal_point_z = []
        
        i=0
        
        while i< 24 * 60:
            
            if y_pred_train[i]==-1:
                anomaly_point_x.append(array[i][0])
                anomaly_point_y.append(array[i][1])    
                #anomaly_point_z.append(array[i][2])
                #print(datakey.get(i))   
            else:
                normal_point_x.append(array[i][0])
                normal_point_y.append(array[i][1])
                #normal_point_z.append(array[i][2])
                
            i+=1
        
        #fig = plt.figure()
        #ax = plt3d.Axes3D(fig)
        
        #ax.scatter(anomaly_point_x, anomaly_point_y, anomaly_point_z, c='red')
        #ax.scatter(normal_point_x, normal_point_y, normal_point_z, c='green')
        
        
        plt.scatter(anomaly_point_x, anomaly_point_y, c='red')
        plt.scatter(normal_point_x, normal_point_y, c='green')

        plt.show()

