# coding: utf8
import sys
import urllib
import urllib2
import cookielib
import re
import pandas as pd
import time
import datetime
import csv

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


def getexcel(url, para_dict):
    cookie = cookielib.MozillaCookieJar()
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    handler = urllib2.HTTPCookieProcessor(cookie)

    opener = urllib2.build_opener(handler)
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"),
                         ("Connection", "Keep-Alive"), ("Host", "10.245.5.217:10107"),
                         ("Accept-Encoding", "gzip, deflate"),
                         ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")]
    urllib2.install_opener(opener)
    para_data = urllib.urlencode(para_dict)
    req = urllib2.Request(url, para_data)
    req.add_header("Referer",
                   "http://10.245.5.217:10107/MRC/mrc.rc.report.display.do?id=17050414222987&reportParamsId=112597")
    # try:
    res = urllib2.urlopen(req)

    # except urllib2.URLError, e:
    #     print e.code
    print res.geturl()
    # print res.info()
    # print res.read()
    # pattern = re.compile(r'".*"')
    # match = pattern.search(str(res.read()))
    ss = res.read()
    match1 = re.search(r'".*"', ss, re.M)
    # match2 = re.search(r'".*"',
    #                    '<script language=javascript>document.location = "http://10.245.5.217:10107/MRC/ mrc.rc.report.display.do?id = 17042815164817&reportParamsId=108791";</script>')
    # print match1.group()
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Referer': 'http://10.245.5.217:10107/MRC/reportServlet?action=8'}
    # opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"), (
    #     "Referer", "http://10.245.5.217:10107/MRC/reportServlet?action=8")]
    # urllib2.install_opener(opener)
    ss = match1.group()[1:-1]
    Referer =ss.replace(' ', '')
    # Referer1 = {'Referer1' :Referer}
    # ss1 = urllib.urlencode(Referer1)
    # urllib2.install_opener(opener)
    req = urllib2.Request(Referer)
    req.add_header("Referer",
                   "http://10.245.5.217:10107/MRC/reportServlet?action=8")
    res = urllib2.urlopen(req)
    # print res.geturl()
    return  res.read()
    # if name != 'traffic1':
    #     with open(name + '.txt', 'wb') as w_fh:
    #         w_fh.write(res.read())
    # else:
    #     with open(name + '.csv', 'wb') as w_fh:
    #         w_fh.write(res.read())

url = 'http://10.245.5.217:10107/MRC/reportServlet?action=8'
para_dict = {
    'starttime': '2017-04-03',
    'provincelist': '110',
    'resultPage': '/mrc.rc.report.display.do?id=17050414222987'

}

loading()
csv_reader = csv.reader(open('data.csv'))
with pd.ExcelWriter('result_alltestkk.xlsx') as writer:
    for data1 in csv_reader:
        para_dict['starttime'] = str(data1[0])
        dfs = pd.read_html(getexcel(url, para_dict))[6]
        dfs = dfs[0:15].sort(columns = 4)
        dfs[[4,5,6,7,8,17,9]].to_excel(writer, sheet_name=u'交维态在网率统计表%s'%data1[0])



