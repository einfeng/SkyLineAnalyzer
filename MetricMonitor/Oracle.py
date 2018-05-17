# coding: utf-8

import cx_Oracle
import os
from MetricMonitor import settings
import datetime
import time


class oracle:
    
    def __init__(self):
        self.USER = settings.USER
        self.PASSWORD = settings.PASSWORD
        self.CONNECTSTR = settings.CONNECTSTR
        self.encoding = 'UTF-8'
        self.nencoding = 'UTF-8'
        
        os.environ['path'] = os.environ.get('PATH') + ';' + settings.OCIPATH

    
    def getMetric(self):

        sql = 'select * from bomc.metric_monitor where isused = 1'
            
        return self.oracleQuery(sql)
    
    def getData(self, metric_row, start_time, end_time):

        col_time = metric_row[4]
        col_data = metric_row[5]
        tab_name = metric_row[3]
        cuid = metric_row[6]
        cycle = metric_row[7]
        
        '''
        sql = (
            'select ' + col_time + ',' + col_data + ' from ('
            'select * from ' + tab_name + ' where cuid = ' + str(cuid) + 
            ' and ' + col_time + ' >= sysdate - 1000 - ' + str(cycle) + '/86400'
            ' and ' + col_time + ' < sysdate '
            ' order by ' + col_time + ') where rownum <= 1000'
            )
        '''
        
        sql = (
            'select ' + col_time + ',' + col_data + ' from ('
            'select * from ' + tab_name + ' where ' + col_time + ' >= ' + start_time + 
            ' and ' + col_time + ' < ' + end_time + 
            ' order by ' + col_time + ')'
            )
        
        # print(sql)
            
        return self.oracleQuery(sql)
    
    def saveMetric(self, anomaly_time, anomaly_metric_id, ensemble):
        sql = 'insert into anomaly_metric_esb1 (check_time,anomaly_time,anomaly_metric_id,anomaly_ct,first_hour_average,mean_subtraction_cumulation,stddev_from_average ,stddev_from_moving_average,least_squares,grubbs,histogram_bins,median_absolute_deviation,ks_test) values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)'
        datavalue = [(datetime.datetime.now(), datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(anomaly_time) / 1)), "%Y-%m-%d %H:%M:%S"), int(anomaly_metric_id),int(ensemble.count(True)), str(ensemble[0]), str(ensemble[1]), str(ensemble[2]), str(ensemble[3]), str(ensemble[4]), str(ensemble[5]), str(ensemble[6]), str(ensemble[7]), str(ensemble[8]))]
        
        self.oracleInsert(sql, datavalue)
        
    def oracleQuery(self, sql):
        
        
        con = cx_Oracle.connect(self.USER, self.PASSWORD, self.CONNECTSTR, encoding=self.encoding, nencoding=self.nencoding)
        cursor = con.cursor()
            
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        # print('SQL运行成功：')
        # print(sql)
        
        # print(rows)
        
        cursor.close()
        con.close()
        
        return rows
    
    def oracleInsert(self, sql, datavalue):
                
        con = cx_Oracle.connect(self.USER, self.PASSWORD, self.CONNECTSTR, encoding=self.encoding, nencoding=self.nencoding)
        cursor = con.cursor()
        
        cursor.prepare(sql)
        cursor.executemany(None, datavalue)
        con.commit()
        
        # print('SQL运行成功：')
        # print(sql)
        
        # print(rows)
        
        cursor.close()
        con.close()
