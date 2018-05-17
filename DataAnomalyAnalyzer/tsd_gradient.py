import numpy as np

def getGradient(data):
    
    #return (data[-1][1] - data[0][1])/(data[-1][0] - data[0][0])
    
    array = np.array(data)
    
    return (array[-1,1] - np.mean(array[:,1]))/(array[-1,0] - array[0,0])