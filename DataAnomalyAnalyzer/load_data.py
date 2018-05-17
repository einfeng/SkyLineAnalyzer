# coding: utf-8
'''
Created on 2018年4月9日

@author: zhao-PC
'''
import demjson
import csv
import time

class load_data:

    def json(self, jsonname):

        with open('data/' + jsonname) as f:
            json = f.read()
        
        json_data = (demjson.decode(demjson.decode(json)['data']))[0]['dps']
                
        time = sorted(json_data.keys())
                
        data = []
        
        for t in time:
            data.append((t,json_data[t]))
            
        print('已加载Json数据：' + str(data.__len__()) + '条')
        
        return data
    
        
    def csv(self,csvname):
        
        with open('data/' + csvname) as f:
            csv1 = csv.reader(f)
            
            data = []

            for c in csv1:
                if c[0] != '':
                    timeArray = time.strptime(c[0], "%Y/%m/%d %H:%M")
                    data.append((int(time.mktime(timeArray)),float(c[1])))


            return data


