#!usr/bin/python
# coding: utf8

import sys
import urllib
import urllib2
import cookielib
import time
import datetime
import csv
import os

reload(sys)
sys.setdefaultencoding('utf8')


def loading():
    url = 'http://10.245.0.91:10101/wonop/login_check.action'
    cookie = cookielib.MozillaCookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0")]
    urllib2.install_opener(opener)
    para_dict = {'userId': "chenhb35", 'password': "123"}
    para_data = urllib.urlencode(para_dict)
    req = urllib2.Request(url, para_data)
    res = urllib2.urlopen(req)
    cookie.save('cookie.txt', ignore_discard=True, ignore_expires=True)


def getexcel(url, para_dict, name):
    cookie = cookielib.MozillaCookieJar()
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib2.HTTPCookieProcessor(cookie)

    opener = urllib2.build_opener(handler)
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0")]
    urllib2.install_opener(opener)
    timeflag = time.time()
    timeflag = str(timeflag).split('.')[0]
    str1 = 'maintain_query_' + timeflag
    if name != 'traffic':
        para_dict['key'] = str1
    para_data = urllib.urlencode(para_dict)
    req = urllib2.Request(url, para_data)
    res = urllib2.urlopen(req)
    if os.path.exists('./' + name[:11]) == False:
        print os.getcwd()
        os.makedirs('./' + name[:11])
    if ('traffic1' in name) == False:
        with open(name[1:] + '.xlsx', 'wb') as w_fh:
            w_fh.write(res.read())
    else:
        with open(name[1:] + '.csv', 'wb') as w_fh:
            w_fh.write(res.read())


def open_csv(file='data.csv'):
    csv_reader = csv.reader(open(file))
    ss = ''
    for row in csv_reader:
        ss = ss + '"' + str(row[0]) + ' ' + '00:00:00",'
    return ss[:-1]


start = time.clock()
url = 'http://10.245.0.91:10101/wonop/wonop/config/maintain/query/config_maintain_query_L00805_dataList.action'  # 'http://10.245.0.91:10101/wonop/wonop/config/maintain/query/config_maintain_query_L00805_dataList.action?objectTypeId=L00805&_dc=1492048145390'
para_dict = {
    'export': "true",
    'key': str,
    'isHighWay': "0",
    'collectType': "0",
    'provinceId': "110",
    'cityId': "11001,11002,11003,11004,11005,11006,11007,11008,11009,11010,11011,11012,11013,11014",
    'districtId': "",
    'vendorId': "",
    'sysType': "",
    'lcName': "",
    'btsId': "",
    'localcell': "",
    'date': "2017-04-12",
    'flag': "normal",
    'start': "0",
    'limit': "25",
    'page': "1"
}
url_rru = 'http://10.245.0.91:10101/wonop/wonop/config/maintain/query/config_maintain_query_L00862_dataList.action'
para_dict_rru = {
    'export': 'true',
    'key': 'maintain_query_1492053585139',
    'provinceId': '110',
    'cityId': '11001,11002,11003,11004,11005,11006,11007,11008,11009,11010,11011,11012,11013,11014',
    'districtId': '',
    'btsId': '',
    'flag': 'normal',
    'objectTypeId': 'L00862'
}
url_traffic1 = 'http://10.245.0.91:10101/wonop/wonop/perf/exportDirect.action'
para_dict_traffic1 = {
    'coutnerInfos': '[{"counterId":"LC0068050220376","lcName":"\u7a7a\u53e3\u4e0a\u884c\u4e1a\u52a1\u6d41\u91cf(MByte)","leaf":true,"checked":false,"statType":"\u516c\u5f0f"},{"counterId":"LC0068050220380","lcName":"\u7a7a\u53e3\u4e0b\u884c\u4e1a\u52a1\u6d41\u91cf(MByte)","leaf":true,"checked":false,"statType":"\u516c\u5f0f"}]',
    'levelId': 'L00805',
    'toLevelId': 'L00805',
    'netType': '4',
    'vendorId': '0',
    'timeRange': '{"period":"8","timeList":["2017-4-01 00:00:00","2017-4-02 00:00:00"]}',
    'toPeriod': '8',
    'neRange': '{"targetlevel":"cell","selecttype":"1","servicetype":"","neranges":[{"oids":"\'11001\'","lcnames":"\'\u5357\u5b81\'","level":"city","cityid":"11001"},{"oids":"\'11002\'","lcnames":"\'\u67f3\u5dde\'","level":"city","cityid":"11002"},{"oids":"\'11003\'","lcnames":"\'\u6842\u6797\'","level":"city","cityid":"11003"},{"oids":"\'11004\'","lcnames":"\'\u68a7\u5dde\'","level":"city","cityid":"11004"},{"oids":"\'11005\'","lcnames":"\'\u5317\u6d77\'","level":"city","cityid":"11005"},{"oids":"\'11006\'","lcnames":"\'\u9632\u57ce\u6e2f\'","level":"city","cityid":"11006"},{"oids":"\'11007\'","lcnames":"\'\u94a6\u5dde\'","level":"city","cityid":"11007"},{"oids":"\'11008\'","lcnames":"\'\u8d35\u6e2f\'","level":"city","cityid":"11008"},{"oids":"\'11009\'","lcnames":"\'\u7389\u6797\'","level":"city","cityid":"11009"},{"oids":"\'11010\'","lcnames":"\'\u767e\u8272\'","level":"city","cityid":"11010"},{"oids":"\'11011\'","lcnames":"\'\u8d3a\u5dde\'","level":"city","cityid":"11011"},{"oids":"\'11012\'","lcnames":"\'\u6cb3\u6c60\'","level":"city","cityid":"11012"},{"oids":"\'11013\'","lcnames":"\'\u6765\u5bbe\'","level":"city","cityid":"11013"},{"oids":"\'11014\'","lcnames":"\'\u5d07\u5de6\'","level":"city","cityid":"11014"},{"oids":"\'-1\'","lcnames":"\'\u5176\u5b83\'","level":"city","cityid":"-1"}],"checkedNodePaths":[["11001"],["11002"],["11003"],["11004"],["11005"],["11006"],["11007"],["11008"],["11009"],["11010"],["11011"],["11012"],["11013"],["11014"],["-1"]],"vendor":"0"}',
    'filterGroups': '[]',
    'sysTypes': '0',
    'provinceId': '110',
    'isBhFlag': '0',
    'busyFlag': '1',
    'selectType': '1',
    'sysType': '0'
}


# ISOTIMEFORMAT = '%Y-%m-%d'
# str1 = '{"period":"8","timeList":[' + open_csv() + ']}'
def loop(date1):
    # date1 = '2017-04-25'
    str1 = '{"period":"8","timeList":["%s 00:00:00"]}' % (date1)
    print  str1
    # str2 = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    para_dict_traffic1['timeRange'] = str1
    # para_dict['date'] = yesterday
    para_dict['date'] = date1
    print  date1
    loading()
    getexcel(url_rru, para_dict_rru, '/%s/rru' % (date1))
    getexcel(url, para_dict, '/%s/cell' % (date1))
    getexcel(url_traffic1, para_dict_traffic1, '/%s/traffic1' % (date1))
    end = time.clock()
    print str((end - start) / 60) + 'mins'



csv_reader = csv.reader(open('data.csv'))
for data1 in csv_reader:
    if os.path.exists('%s/traffic1.csv' % data1[0]) is False:
        loop(str(data1[0]))
    else:
        pass
