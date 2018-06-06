# coding: utf-8

import numpy as np
from sklearn import preprocessing
from sklearn import linear_model

def getLinearRegression(data):
    
    np_data = np.array(data)
    
    x = np_data[:, 0]
    y = np_data[:, 1]
        
    linreg = linear_model.LinearRegression()
    linreg.fit(x.reshape(-1, 1), y)
    
    intercept = linreg.intercept_
    coef = linreg.coef_
    
    return coef,intercept
