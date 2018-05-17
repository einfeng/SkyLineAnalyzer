def getGradientRecent(data):
    
    v_mean = 0
    for i in range(-2,-6,-1):
        v_mean += getGradient(data[i], data[-1])
        
    return v_mean/5
    
def getGradient(data_point1,data_point2):
    return (data_point2[1] - data_point1[1])/(data_point2[0] - data_point1[0])