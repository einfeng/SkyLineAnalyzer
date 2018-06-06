# coding: utf-8
"""
Created on 2018年4月11日

@author: zhao-PC
利用前十天相同时间点数据过滤异动
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from DataAnomalyAnalyzer.skyline_algorithms import run_selected_algorithm


def calc():
    data = pd.read_csv('data/busi_yyt.csv', header=None, names=('time', 'value'), parse_dates=['time'],
                       date_parser=(lambda x: pd.datetime.strptime(x, '%Y/%m/%d %H:%M')))

    data_process = data[('2018-03-27' <= data['time']) & (data['time'] < '2018-03-28')]

    window = 30

    point = pd.DataFrame(columns=['time', 'value'])
    ano_point = pd.DataFrame(columns=['time', 'value'])

    for i in range(len(data_process) - window):
        data_window = data_process.iloc[i:i + window]
        data_window['time'] = data_window.apply(lambda x: pd.to_datetime(x['time']).value // (10 ** 9), axis=1)

        anomalous, ensemble, datatime, datapoint = run_selected_algorithm(data_window.values, 'test')

        point['time'].loc[i] = (datatime % 86400) / 3600
        point['value'].loc[i] = datapoint

        if anomalous:
            ano_point['time'].loc[i] = (datatime % 86400) / 3600
            ano_point['value'].loc[i] = datapoint

        print(i)

    plt.figure(figsize=(15, 3))
    plt.plot(point['time'], point['value'])
    plt.scatter(ano_point['time'], ano_point['value'], color='red')
    plt.ylabel('median_absolute_deviation')
    my_x_ticks = np.arange(0, 24, 1)
    plt.xticks(my_x_ticks)
    plt.show()


class SkylineCalc:
    pass
