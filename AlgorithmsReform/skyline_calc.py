# coding=utf-8
#
# 功能：
# 开发人：赵震宇
# 开发时间：2018年5月9日 上午10:41:36
#    
# ####输入参数####
#
# ####返回值####
#

import AlgorithmsReform.load_data as load


def skyline_calc():
    
    ld = load.load_data()
    data = ld.csv('busi_yyt.csv')
    
    print(data)