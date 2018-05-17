# coding: utf-8

from MetricMonitor.algorithms import run_selected_algorithm
from MetricMonitor import settings
from collections import defaultdict
from MetricMonitor import Oracle
import matplotlib.pyplot as plt
import time


class Monitor():

    def getData(self):
        
        oracle = Oracle.oracle()
        
        metric_name = 'test'
        
        metrics = oracle.getMetric()

        self.start_time = '1521043200'
        self.end_time = '1521046800'
        
        all1 = []
        
        i = 1
        while(i <= 1440 * 5):
            all1.append(i)
            i += 1
        
        for i1 in all1:
            for metric in metrics:
                timeseries_tmp = oracle.getData(metric, self.start_time, self.end_time)
                timeseries = []

                for i in timeseries_tmp:
                    # timeseries.append((time.mktime(i[0].timetuple()),i[1]))
                    timeseries.append((i[0], i[1]))
                
                anomaly_breakdown = defaultdict(int)
                
                print(int(i1))
            
                anomalous, ensemble, datatime, datapoint = run_selected_algorithm(timeseries, metric_name)
                
                print(datatime)
                
                # If it's anomalous, add it to list
                
                if anomalous:
                    # base_name = metric_name
                    # metric = [datapoint, base_name]
                    
                    # Get the anomaly breakdown - who returned True?
                    for index, value in enumerate(ensemble):
                        if value:
                            algorithm = settings.ALGORITHMS[index]
                            anomaly_breakdown[algorithm] += 1
                
                if ensemble != None:
                    oracle.saveMetric(self.end_time, metric[0], ensemble)
                
            '''
            list1=[]
            
            for i in timeseries:
                list1.append(i[1])
                    
            plt.plot(list1)
            plt.show()
            '''
            self.start_time = str(int(self.start_time) + 60)
            self.end_time = str(int(self.end_time) + 60)


if __name__ == '__main__':

    Monitor().getData()
