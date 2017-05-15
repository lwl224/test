# -*- coding: utf-8 -*-
"""
__author__ = 'lwl224'
__mtime__ = '2017/5/10'
"""
import sys
import pyfpgrowth

reload(sys)
sys.setdefaultencoding('utf8')

transactions = [[u'南宁', 2, 5],
                [2, 4],
                [2, 3],
                [u'南宁', 2, 4],
                [u'南宁', 3],
                [2, 3],
                [u'南宁', 3],
                [u'南宁', 2, 3, 5],
                [u'南宁', 2, 3]]
patterns = pyfpgrowth.find_frequent_patterns(transactions, 2)
rules = pyfpgrowth.generate_association_rules(patterns, 0.6)

print rules
print '南宁'
print str(patterns)

