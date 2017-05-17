# -*- coding: utf-8 -*-
"""
__author__ = 'lwl224'
__mtime__ = '2017/5/16'
"""
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import csv
from multiprocessing.dummy import Pool as ThreadPool
# from numpy import *
import pandas as pd
import netboot as nn

csv_reader = csv.reader(open('data.csv'))
citys = (101, 113, 127, 128, 124,
         116, 114, 115, 102, 130, 121, 107, 108, 112, 122, 125, 117, 105, 103, 110, 111, 104, 126, 131, 120, 123, 129,
         109, 106, 119, 118)
for datae in csv_reader:
    auto_list = [
        {'starttime': str(y), 'provincelist': str(x), 'resultPage': '/mrc.rc.report.display.do?id=17050414222987'} for x
        in citys for y in datae]
    pool = ThreadPool(4)
    results = pool.map(nn.getexcel1, auto_list)
    results1 = map(pd.read_html, results)
    empty = pd.DataFrame().append(results1[0][6], ignore_index=True)
    empty1 = pd.DataFrame().append(results1[0][6][1:], ignore_index=True)
    for i in results1[1:]:
        empty = empty.append(i[6][1:], ignore_index=True)
        empty1 = empty1.append(i[6][-1:], ignore_index=True)
    results2 = empty
    pool.close()
    pool.join()
    if os.path.exists('./%s' % datae) == False:
        print os.getcwd()
        os.makedirs('./%s' % datae)
    with pd.ExcelWriter('%s/result_allsheng%s.xlsx' % (datae, datae)) as writer:
        empty[[2, 4, 5, 6, 7, 8, 17, 9]].to_excel(writer, sheet_name=u'交维态在网率统计表')
        empty1[[2, 4, 5, 6, 7, 8, 17, 9]].to_excel(writer, sheet_name=u'各省交维态在网率统计表')
