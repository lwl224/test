# coding:utf-8
import codecs
import csv
import os
import sys
from re import sub
from time import clock

from pandas import DataFrame, read_csv, read_excel, to_datetime, merge, ExcelWriter

reload(sys)
sys.setdefaultencoding('utf8')


def subcat(x, y):
    return str(x) + str(y)


def loop(data1):
    if os.path.exists('%s/traffic1.csv' % data1):
        with open('%s/traffic.csv' % data1, 'w') as f1:
            f2 = open('%s/traffic1.csv' % data1, 'r')
            s = f2.read()
            s = sub('charset=gb2312', 'charset=utf-8', s)
            s = s.decode('gbk')
            f1.write(codecs.BOM_UTF8)
            f1.write(s.encode('utf-8'))
            f1.flush()
            f2.close()
    else:
        pass
    start = clock()
    if os.path.exists(ur'%s/traffic.csv' % data1):
        dfl = read_csv(ur'%s/traffic.csv' % data1, skiprows=[0], header=None)
    elif os.path.exists(ur'%s/traffic.xlsx' % data1):
        dfl = read_excel(ur'%s/traffic.xlsx' % data1, skiprows=[0], header=None)
    else:
        pass
    dfr = read_excel(ur'%s/rru.xlsx' % data1, skiprows=[0], header=None)
    dfc = read_excel(ur'%s/cell.xlsx' % data1, skiprows=[0], header=None)
    # dfl = pd.read_excel(ur'traffic.xlsx', skiprows=[0], header=None)
    end = clock()
    print str((end - start) / 60) + 'mins'
    print 'f_excel'
    start = clock()
    dfl[11] = dfl[11].astype(float) + dfl[10].astype(float)
    column1 = dfr.ix[:, [8, 3]]
    column1.columns = ['cellid', 'city']
    temp = dfc.ix[:, [1, 4, 5, 6, 7, 36]]
    temp[6] = temp[6].astype(int)
    temp[1] = temp[6].map(lambda x: '110.{}.'.format(x), na_action=None)
    temp[7] = temp[7].fillna(100000)
    temp[7] = temp[7].astype(int)
    temp[1] = DataFrame(map(lambda x, y: str(x) + str(y), temp[1], temp[7]), columns=[u'nodeid'])
    column2 = temp.ix[:, [1, 4, 5, 36]]
    column2.columns = ['cellid', 'city', 'district', 'state']
    column2 = column2.fillna(u'其他')
    df_null = column2[column2['state'].isnull()]
    df_not_null = column2[column2['state'].notnull()]
    df_not_null_1 = df_not_null[df_not_null['state'].str.contains(u'现网运行状态')]
    df_not_null_2 = df_not_null[df_not_null['state'].str.contains(u'新增网元工程状态')]
    df_not_null_3 = df_not_null[df_not_null['state'].str.contains(u'搬迁工程状态')]
    df_not_null_4 = df_not_null[df_not_null['state'].str.contains(u'替换工程状态')]
    df_not_null_5 = df_not_null[df_not_null['state'].str.contains(u'维护工程状态')]
    df_not_null_6 = df_not_null[df_not_null['state'].str.contains(u'暂时关闭状态')]
    column2 = df_not_null_1
    if df_not_null_3.empty is False:
        column2 = column2.append(df_not_null_3, ignore_index=True)
    if df_not_null_4.empty is False:
        column2 = column2.append(df_not_null_4, ignore_index=True)
    if df_not_null_5.empty is False:
        column2 = column2.append(df_not_null_5, ignore_index=True)
    if df_not_null_6.empty is False:
        column2 = column2.append(df_not_null_6, ignore_index=True)
    if df_null.empty is False:
        column2 = column2.append(df_null, ignore_index=True)
    column2['cellid'] = column2['cellid'].str.replace('\s', '', case=False)
    # column2_new = df_null.append(df_not_null_2, ignore_index=True)
    column2_new = df_not_null_2
    column2_new['cellid'] = column2_new['cellid'].str.replace('\s', '', case=False)
    TEST_Statistical_rru = column1['city'].groupby(column1['cellid']).size()
    TEST_Statistical_rru = TEST_Statistical_rru - 1
    TEST_Statistical_rru = TEST_Statistical_rru.reset_index()
    TEST_Statistical_rru.columns = ['cellid', 'rrunumber1']
    TEST_Statistical_rru['cellid1'] = TEST_Statistical_rru['cellid']
    TEST_Statistical_rru['cellid'] = TEST_Statistical_rru['cellid'].str.replace('\s', '', case=False)
    OnNetRru = merge(column2, TEST_Statistical_rru, how='left', on='cellid')
    OnNetRru = OnNetRru.fillna(0)
    OnNetRru['rrunumber1'] = OnNetRru['rrunumber1'] + 1
    OnNetRru_new = merge(column2_new, TEST_Statistical_rru, how='left', on='cellid')
    OnNetRru_new = OnNetRru_new.fillna(0)
    OnNetRru_new['rrunumber1'] = OnNetRru_new['rrunumber1'] + 1
    column3 = dfl.ix[:, [3, 2, 11, 8, 4]]
    column3 = column3.fillna('其他')
    column3.columns = ['cellid', 'time', 'flow', 'district', 'cellname']
    column3['rrunumber'] = 1
    column3['cellid'] = column3['cellid'].str.replace('\s', '', case=False)
    TEST_Statistical_rru2 = merge(column3, TEST_Statistical_rru, how='left', on='cellid')
    TEST_Statistical_rru2 = TEST_Statistical_rru2.fillna(0)
    TEST_Statistical_rru2['rrunumber1'] = TEST_Statistical_rru2['rrunumber1'].astype(int)
    TEST_Statistical_rru2['rrunumber'] = TEST_Statistical_rru2['rrunumber'] + TEST_Statistical_rru2['rrunumber1']
    column3['rrunumber'] = TEST_Statistical_rru2['rrunumber']
    column3['time'] = to_datetime(column3['time'])
    OnNetCell = column3[column3['cellid'].isin(set(OnNetRru['cellid'].astype(str)))]
    OnNetCell_new = column3[column3['cellid'].isin(set(OnNetRru_new['cellid']))]
    NotNetCell = column3[~column3['cellid'].isin(set(OnNetRru['cellid']))]
    NotNetCell_new = column3[~column3['cellid'].isin(set(OnNetRru_new['cellid']))]
    NotNetRRU = OnNetRru[~OnNetRru['cellid'].isin(set(column3['cellid']))]
    NotNetRRU_new = OnNetRru_new[~OnNetRru_new['cellid'].isin(set(column3['cellid']))]
    WorkCell = OnNetCell[OnNetCell['flow'] > 0]
    WorkCell_new = OnNetCell_new[OnNetCell_new['flow'] > 0]
    Statistical_rru = OnNetRru['rrunumber1'].groupby(OnNetRru['city']).sum()
    Statistical_rru3 = OnNetRru['rrunumber1'].groupby(OnNetRru['district']).sum()

    Statistical_rru_new = OnNetRru_new['rrunumber1'].groupby(OnNetRru_new['city']).sum()
    Statistical_rru = DataFrame(Statistical_rru)
    Statistical_rru3 = DataFrame(Statistical_rru3)
    Statistical_rru.columns = [u'交维态RRU总数']
    Statistical_rru3.columns = [u'交维态各区县RRU总数']
    Statistical_rru_new = DataFrame(Statistical_rru_new)
    Statistical_rru_new.columns = [u'新增态RRU总数']
    Statistical_groupby = merge(OnNetRru, OnNetCell, on='cellid')
    Statistical_groupby_new = merge(OnNetRru_new, OnNetCell_new, on='cellid')
    Statistical_groupby_zero = Statistical_groupby[Statistical_groupby['flow'] == 0]
    Statistical_groupby = Statistical_groupby[Statistical_groupby['flow'] > 0]
    Statistical_groupby_new_zero = Statistical_groupby_new[Statistical_groupby_new['flow'] == 0]
    Statistical_groupby_new = Statistical_groupby_new[Statistical_groupby_new['flow'] > 0]
    Statistical_groupby_zero_1 = Statistical_groupby_zero['rrunumber'].groupby(
        [Statistical_groupby_zero['city'], Statistical_groupby_zero['cellid']]).sum()
    # Statistical_groupby2 = Statistical_groupby['cellid'].groupby(Statistical_groupby['city']).size()
    Statistical_groupby2 = Statistical_groupby['rrunumber'].groupby(Statistical_groupby['city']).sum()
    Statistical_groupby3 = Statistical_groupby['rrunumber'].groupby(Statistical_groupby['district']).sum()
    Statistical_groupby3 = DataFrame(Statistical_groupby3)
    Statistical_groupby_new_zero_1 = Statistical_groupby_new_zero['rrunumber'].groupby(
        Statistical_groupby_new_zero['cellid']).sum()
    Statistical_groupby2_new = Statistical_groupby_new['rrunumber'].groupby(Statistical_groupby_new['city']).sum()
    Statistical_groupby2 = DataFrame(Statistical_groupby2,
                                     index=[u'百色市', u'北海市', u'崇左市', u'防城港市', u'贵港市', u'桂林市', u'河池市', u'贺州市', u'来宾市',
                                            u'柳州市',
                                            u'南宁市', u'钦州市', u'梧州市', u'玉林市'])
    Statistical_groupby2.columns = [u'交维态在网RRU数']
    Statistical_groupby3.columns = [u'交维态在网RRU数']
    Statistical_groupby_zero_1 = DataFrame(Statistical_groupby_zero_1)
    Statistical_groupby_zero_1.columns = [u'交维态在网RRU数']
    Statistical_groupby_new_zero_1 = DataFrame(Statistical_groupby_new_zero_1, columns=[u'交维态在网RRU数'])

    Statistical_groupby2_new = DataFrame(Statistical_groupby2_new)
    Statistical_groupby2_new.columns = [u'新增态在网RRU数']
    num = int(len(set(column3['time'])))
    Statistical_groupby2[u'交维态RRU总数'] = Statistical_rru
    Statistical_groupby3[u'交维态各区县RRU总数'] = Statistical_rru3
    Statistical_groupby2[u'交维态在网率'] = Statistical_groupby2[u'交维态在网RRU数'] / (Statistical_rru[u'交维态RRU总数'] * num)
    Statistical_groupby3[u'交维态在网率'] = Statistical_groupby3[u'交维态在网RRU数'] / (Statistical_rru3[u'交维态各区县RRU总数'] * num)
    Statistical_groupby2[u'交维态在网RRU数'] = Statistical_groupby2[u'交维态在网RRU数'] / num
    Statistical_groupby3[u'交维态在网RRU数'] = Statistical_groupby3[u'交维态在网RRU数'] / num
    Statistical_groupby2[u'新增态在网RRU数'] = Statistical_groupby2_new
    Statistical_groupby2[u'新增态RRU总数'] = Statistical_rru_new
    Statistical_groupby2[u'新增态在网率'] = Statistical_groupby2[u'新增态在网RRU数'] / (Statistical_rru_new[u'新增态RRU总数'] * num)
    Statistical_groupby2[u'新增态在网RRU数'] = Statistical_groupby2[u'新增态在网RRU数'] / num
    Statistical_groupby2[u'新增态在网RRU数'] = Statistical_groupby2[u'新增态在网RRU数'].fillna(0)
    Statistical_groupby2[u'新增态在网率'] = Statistical_groupby2[u'新增态在网率'].fillna(0)
    Statistical_groupby2[u'新增态RRU总数'] = Statistical_groupby2[u'新增态RRU总数'].fillna(0)
    with ExcelWriter('%s/result_alltest%s.xlsx' % (data1, data1)) as writer:
        Statistical_groupby2.to_excel(writer, sheet_name=u'交维态在网率统计表')
        OnNetRru.to_excel(writer, sheet_name=u'交维态在网RRU总数清单')
        NotNetRRU.to_excel(writer, sheet_name=u'没有对应流量指标的RRU清单')
        OnNetRru_new.to_excel(writer, sheet_name=u'新增态在网RRU总数清单')
        OnNetCell.to_excel(writer, sheet_name=u'交维态有流量RRU清单')
        Statistical_groupby_zero.to_excel(writer, sheet_name=u'交维态没有流量RRU清单')
        Statistical_groupby_zero_1.to_excel(writer, sheet_name=u'交维态没有流量RRU清单统计')
        Statistical_groupby_new_zero.to_excel(writer, sheet_name=u'新增态没有流量RRU清单')
        Statistical_groupby3.to_excel(writer, sheet_name=u'交维态各区县在网率统计表')
    end = clock()
    print str((end - start) / 60) + 'mins'


def saveexcel():
    cst_readall = csv.reader(open('data.csv'))
    writer = ExcelWriter('result_all.xlsx')
    for selctdata in cst_readall:
        dfl = read_excel(ur'%s/result_alltest%s.xlsx' % (selctdata[0], selctdata[0]))
        dfl.to_excel(writer, u'%s交维态在网率统计表' % selctdata[0])
    writer.save()


def saveexcel1():
    cst_readall = csv.reader(open('data.csv'))
    writer = ExcelWriter('result_all_1.xlsx')
    column = DataFrame(columns=['cellid', 'city', 'state', 'rrunumber1', 'cellid1', 'time', 'flow', 'rrunumber'])
    start = clock()
    for selctdata1 in cst_readall:
        dfl = read_excel(ur'%s/result_alltest%s.xlsx' % (selctdata1[0], selctdata1[0]), sheetname=5)
        column = column.append(dfl, ignore_index=True)
        end = clock()
        print str((end - start) / 60) + 'mins'
    column.to_excel(writer, u'交维态在网RRU零话务合计')

    writer.save()


def kkl():
    dfl = read_excel('result_all_1.xlsx', skiprows=[0], header=None)
    dfl.columns = ['k', 'cellid', 'city', 'state', 'rrunumber1', 'cellid1', 'time', 'flow', 'rrunumber']
    def1 = dfl['city'].groupby(dfl['cellid']).size()
    def1 = def1.reset_index()
    def2 = merge(dfl, def1, how='left', on='cellid')
    with ExcelWriter('result_all_2.xlsx') as writer:
        def2.to_excel(writer, sheet_name=u'交维态在网RRU总数清单')


csv_reader = csv.reader(open('data.csv'))
for data1 in csv_reader:
    if os.path.exists('%s/result_alltest%s.xlsx' % (data1[0], data1[0])) is False:
        loop(str(data1[0]))
# saveexcel1()
# kkl()
