# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import DataAnomalyAnalyzer.load_data as ld

from sklearn import svm
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


class algorithms_test():

    def algorithms_test(self):
        
        
        load = ld.load_data()
        
        data1 = load.csv('data_3.csv')
        data2 = load.csv('data_2.csv')
        
        data1_new = []
        data2_new = []

        '''
        for d in data1:
            data1_new.append(d[1])
            
        for d in data2:
            data2_new.append(d[1])            
        '''
        
        for d in data1:
            data1_new.append(d[0])
            data2_new.append(d[1])         
        
        data = zip(data1_new, data2_new)
        
        print(data)
        
        array = np.array(data)   
        '''
        rng = np.random.RandomState(42000)

        array = 0.3 * rng.randn(1000, 2)
        '''
        
        classifiers = {"One-Class SVM": svm.OneClassSVM(),"Robust covariance": EllipticEnvelope(),"Isolation Forest": IsolationForest(),"Local Outlier Factor": LocalOutlierFactor()}
        plt.figure(figsize=(150,150))

        for n, (clf_name, clf) in enumerate(classifiers.items()):
            
            if clf_name == "Local Outlier Factor":
                y_pred = clf.fit_predict(array)
            else:
                clf.fit(array)
                y_pred = clf.predict(array)
            
            anomaly_point_x = []
            anomaly_point_y = []
            normal_point_x = []
            normal_point_y = []
            
            i = 0
            
            while i < 60:
                
                if y_pred[i] == -1:
                    anomaly_point_x.append(array[i][0])
                    anomaly_point_y.append(array[i][1])    
                    # anomaly_point_z.append(array[i][2])
                    # print(datakey.get(i))   
                else:
                    normal_point_x.append(array[i][0])
                    normal_point_y.append(array[i][1])
                    # normal_point_z.append(array[i][2])
                    
                i += 1
            
            plt.subplot(2,2,n + 1)
            plt.title(clf_name)
            
            plt.scatter(anomaly_point_x, anomaly_point_y, c='red')
            plt.scatter(normal_point_x, normal_point_y, c='green')
            
        plt.show()

if __name__ == '__main__':

    algorithms_test().algorithms_test()