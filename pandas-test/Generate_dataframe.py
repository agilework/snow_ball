__author__ = 'admin'
#-*- coding: utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series
import time
import datetime
from datetime import date,timedelta
# dataframe_1 = pd.DataFrame({'A':['foo','bar','foo','bar','foo','bar','foo','foo'],
#                             'B':['one','two','three','four','two','one','three','three'],
#                             'C':np.random.randn(8),'D':np.random.randn(8)})
# print dataframe_1
# print dataframe_1.groupby('A').sum()
#
# dates = pd.date_range('20140404',periods=6)
# dataframe_2 = pd.DataFrame(np.random.randn(6,4),index=dates,columns=['a','b','c','d'])
# print dataframe_2
# print dataframe_2.head(2)
# print dataframe_2.tail(2)
# print dataframe_2.head()
# print dataframe_2.tail()
# print dataframe_2[0:-1]
# print len(dataframe_2.columns)
# print dataframe_2['a'].sum()
#
#
# dataframe_3 = Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
# print dataframe_3.reindex([range(6)],method='bfill')
#
# dataframe_4 = Series(np.arange(4.), index=['a', 'b', 'c', 'd'])
# print dataframe_4[2:4]
#
# dataframe_2.append()
# pd.read_csv()
# now = datetime.datetime.now()
# print now+datetime.timedelta(-1)
# print now
# print type(str(date.today()-timedelta(days=1))+" 15:00")
# s = str(date.today()-timedelta(days=1))+" 15:00"
# print int(time.mktime(time.strptime(s,"%Y-%m-%d %H:%M")))

dict = {"a" : "apple", "b" : "banana", "c" : "grape", "d" : "orange"}
print dict.values()

print time.time()

# data_frame_5 = pd.DataFrame(np.random.randn(6,4))
# print data_frame_5
# data_frame_5.ix[1,2]='NaN'
# print data_frame_5
# print data_frame_5.fillna()

today = datetime.date.today()
print today
print today-datetime.timedelta(days=1)
print '中文'
a = {u'中文':'s'}
print str(a).decode('unicode-escape').encode('utf-8')

g = "[{'a':1},{'c':2}]"
print type(eval(g))
g_b = eval(g)
print g_b[0]

