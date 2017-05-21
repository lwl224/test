# -*- coding: utf-8 -*-
"""
__author__ = 'lwl224'
__mtime__ = '2017/5/16'
"""
import os
import sys
from time import clock

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
guangxicity = (110)
kk = 1
nn.loading()
for datae in csv_reader:
    start = clock()
    auto_list = [
        {'starttime': str(y), 'provincelist': str(x), 'resultPage': '/mrc.rc.report.display.do?id=17050414222987'} for x
        in citys for y in datae]
    para_dict = [
        {'starttime': str(y), 'provincelist': '110', 'resultPage': '/mrc.rc.report.display.do?id=17050414222987'}  for y in datae]
    guanxi = pd.read_html(nn.getexcel1(para_dict[0]))[6]
    pool = ThreadPool(4)
    results = pool.map(nn.getexcel1, auto_list)
    results1 = map(pd.read_html, results)
    empty = pd.DataFrame().append(results1[0][6][0:1], ignore_index=True)
    empty1 = pd.DataFrame().append(results1[0][6][0:1], ignore_index=True)
    for i in results1:
        empty = empty.append(i[6][1:-1], ignore_index=True)
        empty1 = empty1.append(i[6][-1:], ignore_index=True)
    results2 = empty
    pool.close()
    pool.join()
    if os.path.exists('./%s' % datae[0]) == False:
        print os.getcwd()
        os.makedirs('./%s' % datae[0])
    with pd.ExcelWriter('%s/result_allsheng%s.xlsx' % (datae[0], datae[0])) as writer:
        empty[[2, 4, 5, 6, 7, 8, 17, 9]].to_excel(writer, sheet_name=u'交维态在网率统计表')
        empty1[[2, 4, 5, 6, 7, 8, 17, 9]].to_excel(writer, sheet_name=u'各省交维态在网率统计表')
    with pd.ExcelWriter('%s/result_allguangxi%s.xlsx' % (datae[0], datae[0])) as writer:
        guanxi[[2, 4, 5, 6, 7, 8, 17, 9]].to_excel(writer, sheet_name=u'交维态在网率统计表')
    kk +=1
    end = clock()
    print str((end - start) / 60) + 'mins'
i =0
csv_reader = csv.reader(open('data.csv'))
for datae in csv_reader:
    dfr = pd.read_excel('%s/result_allguangxi%s.xlsx' % (datae[0], datae[0]), skiprows=[0,1], header=None)
    dfr=dfr.fillna(u'其他')
    dfr.index = dfr[2].tolist()
    dfr1 = dfr[[7,5,8]]
    dfr1.columns = [ u'存在业务小区数',u'在网RRU数',u'在服率']
    if i ==0 :
        emp = dfr1
        i=i+1
    else:
        emp = emp +dfr1
emp = emp /kk
with pd.ExcelWriter('result_allguangxi.xlsx') as writer:
    emp.to_excel(writer, sheet_name=u'交维态在网率统计表')