# coding:utf-8
from pandas import DataFrame, read_csv, read_excel, to_datetime, merge, ExcelWriter, read_sql
from time import clock
from re import sub
import codecs
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')


def makedata(sql):
    connect_dict = {
        'host': '133.0.31.14',
        'user': 'WGZX',
        'passwd': 'Aa123!@#',
        'port': 3306,
        'db': 'eprocess',
        'use_unicode': 'True',
        'charset': 'utf8'
    }
    conn = MySQLdb.connect(**connect_dict)
    date = read_sql(sql, con=conn)
    conn.close()
    return date


def makeexcel(date):
    result = date.ix[:, ['neName', 'alarmTitle', 'alarmCreateTime', 'RecoveryTime']]
    with ExcelWriter(r'mysqltest.xlsx') as writer:
        result.to_excel(writer, sheet_name='1')


dfc = read_excel(ur'zero.xlsx', skiprows=[0], header=None)
dfb = read_excel(ur'enondb.xlsx', skiprows=[0], header=None)
enondb = dfb.ix[:, [0, 2, 4, 5, 6]]
enondb.columns = ['eNodeB', 'enodeb', 'city', 'region', 'enodebid']
cell = dfc.ix[:, [2, 1, 0]]
cell.columns = ['enodebid', 'day', 'cellid']
cellname = merge(cell, enondb, on='enodebid')
setname = set(cellname['enodeb'])
setname1 = set(cellname['eNodeB'])

ss1 = '('
ss2 = ' Like '
ss3 = ' Like '
for name in setname:
    ss1 = ss1 + '\'' + name + '\','
    ss2 = ss2 + '\'%' + name + '%\' or  ' + u'故障描述' + ' Like '
for name in setname1:
    ss3 = ss3 + '\'%' + name + '%\' or  ' + u'故障描述' + ' Like '


ss1 = ss1[:-1] + ')'
ss2 = ss2[:-14]
ss3 = ss3[:-14]
sql1 = 'SELECT *, timestampdiff( DAY,alarmCreateTime,( CASE WHEN RecoveryTime is NULL  THEN now()  ELSE  RecoveryTime end )) AS diff_time FROM WGZX_view_fault_alarm WHERE neName in' + ss1 + 'and alarmCreateTime BETWEEN \'2017-03-10 00:00:00\' AND \'2017-04-22 00:00:00\' HAVING diff_time > 1  ;'
data1 = makedata(sql1)
result1 = data1.ix[:, ['neName', 'alarmTitle', 'alarmCreateTime','RecoveryTime']]
sql2 = 'SELECT *, timestampdiff( DAY,' + u'出现时间' + ',( CASE WHEN ' + u'回单时间' + ' is NULL  THEN now()  ELSE  ' + u'回单时间' + ' end )) AS diff_time FROM WGZX_view_fault_order_info_report WHERE (' + u'故障描述' + ss2 + ') and ' + u'出现时间' + ' BETWEEN \'2017-04-01 00:00:00\' AND \'2017-04-22 12:00:00\'   ;'
data2 = makedata(sql2)
result2 = data2.ix[:, ['基站名称', '故障类型', '故障描述', '出现时间', '恢复时间']]
sql3 = 'SELECT *, timestampdiff( DAY,' + u'出现时间' + ',( CASE WHEN ' + u'回单时间' + ' is NULL  THEN now()  ELSE  ' + u'回单时间' + ' end )) AS diff_time FROM WGZX_view_fault_order_info_report WHERE (' + u'故障描述' + ss3 + ') and ' + u'出现时间' + ' BETWEEN \'2017-04-01 00:00:00\' AND \'2017-04-22 12:00:00\'   ;'
data3 = makedata(sql3)
result3 = data3.ix[:, ['基站名称', '故障类型', '故障描述', '出现时间', '恢复时间']]
result2.append(result3, ignore_index=True)
with ExcelWriter('result_cellname4_25_3.xlsx') as writer:
    cellname.to_excel(writer, sheet_name=u'cellname')
    cell.to_excel(writer, sheet_name=u'cell')
    result1.to_excel(writer, sheet_name=u'sql1')
    result2.to_excel(writer, sheet_name=u'sql2')
