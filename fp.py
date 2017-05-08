# -*-coding:utf-8-*-
'''
Created on 2016年5月9日
@author: Gamer Think
'''

import MySQLdb
import pandas as pd
import sys
import time

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def custom_resampler(array_like):
    if 1 > 0:
        return array_like.str.cat(sep=',')
    else:
        return array_like


def makedata():
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
    # cur = conn.cursor()
    # print(conn)
    # print(cur)
    namelist = ['兴安县', '玉东区', '环江县', '大化县', '田东县', '右江城郊', '兴宾区', '昭平县', '金秀县', '凭祥市', '钦州港', '隆安县', '港北区', '邕宁区',
                '藤县县',
                '合浦县', '青秀北区', '贵港市区', '象州县', '北流市', '武鸣县', '马山县', '长洲区', '平南县', '西乡塘区', '东兴市', '桂平县', '田林县', '凤山县',
                '院校区',
                '江州区', '隆林县', '灵山县', '岑溪县', '田阳县', '乐业县', '龙州县', '天峨县', '永福县', '靖西县', '全州县', '柳北区', '青秀区', '宜州市', '兴业县',
                '桂林雁山', '临桂县', '江南区', '防城区', '南丹县', '梧州市区', '武宣县', '东兰县', '陆川县', '桂林叠彩', '富川县', '灵川县', '钦州城区', '北海城东',
                '平乐县', '桂林秀峰', '柳江县', '荔浦县', '平果县', '上思县', '玉州区', '来宾城郊', '忻城县', '融水县', '来宾城区', '桂林七星', '藤县', '鹿寨县',
                '铁山港区',
                '阳朔县', '青秀南区', '河池中心机房', '博白县', '恭城县', '三江县', '兴宁区', '港口区', '海城区', '柳州市区', '苍梧县', '西林县', '右江区', '南宁市',
                '柳南区', '容县', '那坡县', '宾阳县', '平桂区', '扶绥县', '天等县', '崇左市区', '百色市区', '福绵区', '浦北县', '柳东区', '港南区', '龙胜县',
                '合山市',
                '桂林象山', '都安县', '玉林市区', '横县', '德保县', '八步区', '桂林院校', '宁明县', '凌云县', '资源县', '巴马县', '北海城西', '鱼峰区', '山口片区',
                '万秀区',
                '贺州市区', '覃塘区', '五象新区', '玉林', '蒙山县', '金城江', '灌阳县', '良庆区', '罗城县', '上林县', '北流县', '大新县', '融安县', '钟山县',
                '柳城县']
    sql = "SELECT distinct WGZX_view_fault_order_info_report.故障编号,WGZX_view_fault_order_info_report.基站名称,WGZX_view_fault_alarm.neName,WGZX_view_fault_order_info_report.出现时间 , WGZX_view_fault_order_info_report.回单时间 ,timestampdiff(MINUTE,WGZX_view_fault_order_info_report.出现时间,(CASE WHEN WGZX_view_fault_order_info_report.工单状态='已恢复' THEN WGZX_view_fault_order_info_report.回单时间 ELSE now() END))AS diff_time ,WGZX_view_fault_alarm.RecoveryTime,WGZX_view_fault_order_info_report.区域,WGZX_view_fault_order_info_report.地市,WGZX_view_fault_alarm.alarmCreateTime FROM WGZX_view_fault_order_info_report Left JOIN WGZX_view_fault_alarm  ON WGZX_view_fault_alarm.CorrespondingAccept=WGZX_view_fault_order_info_report.故障编号 WHERE WGZX_view_fault_order_info_report.工单状态 NOT IN ('不处理') AND WGZX_view_fault_order_info_report.故障类型='基站退服' AND WGZX_view_fault_order_info_report.区域 ='右江区'AND 出现时间 BETWEEN '2016-01-01 00:00:00' AND '2017-01-01 00:00:00' AND WGZX_view_fault_alarm.alarmCreateTime IS NOT  null ORDER  BY 故障编号 ASC , 基站名称 DESC ,出现时间 ASC "
    date = pd.read_sql(sql, con=conn)
    conn.close()
    return date


def makeexcel(date):
    date['RecoveryTime'] = pd.to_datetime(date['RecoveryTime'])
    date['alarmCreateTime'] = pd.to_datetime(date['alarmCreateTime'])
    date['neName'] = date['neName'].str.strip()
    date.set_index('alarmCreateTime')
    date.index = date['alarmCreateTime'].tolist()
    var1 = date[['neName', '地市', '区域']].resample('30min', how=custom_resampler)
    var2 = var1.groupby(var1['区域']).size()
    var2 = pd.DataFrame(var2)
    # data1 = str(data1).decode("unicode-escape").encode("utf-8")
    # print data1
    # for name in namelist:
    #     var1 = date[['neName', '地市', '区域']][date['区域'] == name]
    #     if var1.empty != True:
    #         var1 = var1.resample('2H', how=custom_resampler)
    #         testdata = pd.DataFrame(var1)
    #         if testdata.empty:
    #             testdata = pd.DataFrame(var1)
    #         else:
    #             testdata.append(var1)
    # var2=date['区域'].resample('2H',how=custom_resampler)
    # date2 = pd.DataFrame([var1, var2])
    # date2= date2.T
    # cur.execute(sql)
    # result_set = cur.fetchall()
    # if result_set:
    #     for row in result_set:
    #         print "%s, %s, %s, %s, %s, %s" % (row[0],row[1],row[2],row[3],row[4],row[5])
    #
    # cur.close()
    # conn.close()
    with pd.ExcelWriter(r'mysqltest.xlsx') as writer:
        var1.to_excel(writer, sheet_name='1')
        date.to_excel(writer, sheet_name='2')
        var2.to_excel(writer, sheet_name='3')


# 定义一个树，保存树的每一个结点
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.parent = parentNode
        self.children = {}  # 用于存放节点的子节点
        self.nodeLink = None  # 用于连接相似的元素项

    # 对count变量增加给定值
    def inc(self, numOccur):
        self.count += numOccur

    # 用于将树以文本形式显示，对于构建树来说并不是需要的
    def disp(self, ind=1):
        print "  " * ind, self.name, "  ", self.count
        for child in self.children.values():
            child.disp(ind + 1)


# FP树的构建函数
def createTree(dataSet, minSup=1):
    ''' 创建FP树 '''
    # 第一次遍历数据集，创建头指针表
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # 移除不满足最小支持度的元素项
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del (headerTable[k])
    # 空元素集，返回空
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    # 增加一个数据项，用于存放指向相似元素项指针
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None)  # 根节点
    # 第二次遍历数据集，创建FP树
    for tranSet, count in dataSet.items():
        localD = {}  # 对一个项集tranSet，记录其中每个元素项的全局频率，用于排序
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]  # 注意这个[0]，因为之前加过一个数据项
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]  # 排序
            updateTree(orderedItems, retTree, headerTable, count)  # 更新FP树
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    # 判断事务中的第一个元素项是否作为子节点存在，如果存在则更新该元素项的计数
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    # 如果不存在，则创建一个新的treeeNode并将其作为子节点添加到树中
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # 更新头指针表或前一个相似元素项节点的指针指向新节点
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
            # 对剩下的元素项迭代调用updateTree函数
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

        # 获取头指针表中该元素项对应的单链表的尾节点，然后将其指向新节点targetNode


def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# 生成数据集
def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


# =========================================================

# 给定元素项生成一个条件模式基（前缀路径）
# basePat表示输入的频繁项，treeNode为当前FP树中对应的第一个节点（可在函数外部通过headerTable[basePat][1]获取）
def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    # 返回函数的条件模式基
    return condPats


# 辅助函数，直接修改prefixPath的值，将当前节点leafNode添加到prefixPath的末尾，然后递归添加其父节点
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

        # 递归查找频繁项集


# 参数：inTree和headerTable是由createTree()函数生成的数据集的FP树
#    : minSup表示最小支持度
#    ：preFix请传入一个空集合（set([])），将在函数中用于保存当前前缀
#    ：freqItemList请传入一个空列表（[]），将用来储存生成的频繁项集
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myConTree, myHead = createTree(condPattBases, minSup)

        if myHead != None:
            # 用于测试
            print 'conditional tree for :', newFreqSet
            myConTree.disp()

            mineTree(myConTree, myHead, minSup, newFreqSet, freqItemList)


def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            # issubset：表示如果集合can中的每一元素都在tid中则返回true
            if can.issubset(tid):
                # 统计各个集合scan出现的次数，存入ssCnt字典中，字典的key是集合，value是统计出现的次数
                if not ssCnt.has_key(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        # 计算每个项集的支持度，如果满足条件则把该项集加入到retList列表中
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        # 构建支持的项集的字典
        supportData[key] = support
    return retList, supportData


def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            # issubset：表示如果集合can中的每一元素都在tid中则返回true
            if can.issubset(tid):
                # 统计各个集合scan出现的次数，存入ssCnt字典中，字典的key是集合，value是统计出现的次数
                if not ssCnt.has_key(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        # 计算每个项集的支持度，如果满足条件则把该项集加入到retList列表中
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        # 构建支持的项集的字典
        supportData[key] = support
    return retList, supportData


# 封装算法
def fpGrowth(dataSet, minSup=3):
    initSet = createInitSet(dataSet)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    freqItems = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
    return freqItems


if __name__ == "__main__":
    # 测试加载数据集和生成树代码
    '''
    simpDat = loadSimpDat()
    initSet = createInitSet(simpDat)
    myFPtree, myHeaderTab = createTree(initSet, 3)
    print myFPtree.disp()
    '''
    # 测试findPrefixPath代码
    '''
    print "x",findPrefixPath('x', myHeaderTab['x'][1])
    print "z",findPrefixPath('z', myHeaderTab['z'][1])
    print "r",findPrefixPath('r', myHeaderTab['r'][1])
    '''
    # 测试mineTree的代码
    '''
    freqItems = []
    mineTree(myFPtree,  myHeaderTab, 3, set([]), freqItems)
    print freqItems
    '''
    # 封装算法后代码测试
    makeexcel(makedata())
    print(u'\n转换原始数据至0-1矩阵...')
    start = time.clock()
    d1 = pd.read_excel('mysqltest.xlsx', skiprows=[0], header=None)
    d2 = d1[d1[1].notnull()]
    d2['test'] = d2[1].str.split(',')
    dd = d2['test'][len(d2['test'].values)>1]
    num1 = map(set, d2['test'])
    num1 = map(list, num1)
    # dataSet = loadSimpDat()
    freqItems = fpGrowth(num1)
    freqItems = str(freqItems).decode("unicode-escape").encode("utf-8")
    Lk, supK = scanD(num1, freqItems, 0.07)

    print str(freqItems).decode("unicode-escape").encode("utf-8")
