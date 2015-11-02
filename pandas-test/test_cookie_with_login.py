__author__ = 'admin'
#-*- coding:utf8 -*-
import urllib2
import requests
def login():
    headers = {"Host":"xueqiu.com","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0",\
               "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"\
               }
    url = 'http://xueqiu.com/'
    r = requests.get(url,headers=headers)
    print r.headers

if __name__ == '__main__':
    login()
