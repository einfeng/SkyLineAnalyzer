import numpy as np
from sklearn import preprocessing

def getScaler(data):

    np_data = np.array(data)

    min_max_scaler = preprocessing.MinMaxScaler()
    data_new = min_max_scaler.fit_transform(np_data.reshape(-1, 1))
    
    return data_new