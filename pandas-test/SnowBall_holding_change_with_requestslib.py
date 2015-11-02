__author__ = 'admin'
#-*- coding: utf-8 -*-
#寻找某段时间内总体盈利排行中，每个人在当天的持股变化
from string import  Template
import time
import datetime
from datetime import date,timedelta
from bs4 import BeautifulSoup
import  cookielib
import urllib2
import urllib
import json
import requests

class HoldChangeByProfit:

    urls = []
    hold_map = {}
    single_html_content = []
    hold_change_map = {}
    cookies = None
    #得到所有持股人的页面url
    def get_Hold_Page(self):
        template = Template("http://xueqiu.com/cubes/discover/rank/cube/list.json?market=cn&sale_flag=0&stock_positions=0&sort=best_benefit&category=12&profit=annualized_gain_rate&page=$a&count=$b")
        #我默认是取的三页的数据，可以修改的
        base_page = range(1,31)
        for i in base_page:
            page = int(i)
            count = int(i)*10
            HoldChangeByProfit.urls.append(template.substitute(a=str(page),b=str(count)))
    #得到单个持股人的信息
    def get_single_hold_url(self):
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',\
                   #'cookie':'s=v2x115hqe7; xq_a_token=ec225cc39134e9d7f331b34986471ab8a38b97c4; \
                   #xq_r_token=72976e9c8f5ac083b294f89b658188b16f43bdb9'}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'}
        if(len(HoldChangeByProfit.urls) == 0):
            print '没有最赚钱组合的urls!'
            exit(-1)
        for url in HoldChangeByProfit.urls:
            try:
                print url
                break
                #opener = self.login()
                #request = urllib2.Request(url,headers=headers)
                seesion = self.login()
                print type(seesion)
                #r = seesion.post(url, headers=headers, cookies=HoldChangeByProfit.cookies)
                r = seesion.post(url)
                #json_content = r.json()
                print 'content is '+str(r.text)
                #print opener.open(request).read()
                #json_content = json.loads(self.login().open(url).read())
                # hold_list = json_content.get("list")
                # for j in hold_list:
                #     HoldChangeByProfit.hold_map[j['name']]=j['symbol']
            except Exception,e:
                print 1
                print e
    #得到每个持股人的页面数据
    def get_all_hold_page_content(self):
        #得到昨天下午三点后的时间戳
        yesterday_time = int(time.mktime(time.strptime(str(date.today()-timedelta(days=1))+" 15:00","%Y-%m-%d %H:%M")))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',\
                   'cookie':'s=v2x115hqe7; xq_a_token=ec225cc39134e9d7f331b34986471ab8a38b97c4; \
                   xq_r_token=72976e9c8f5ac083b294f89b658188b16f43bdb9'}

        base_url_template = Template("http://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=$a&count=20&page=1")
        print HoldChangeByProfit.hold_map.values()
        for single_info in HoldChangeByProfit.hold_map.values():
            print 'start to get ticket data page : '+single_info
            hold_change_tuple = []
            url = base_url_template.substitute(a=single_info)
            request = urllib2.Request(url, headers=headers)
            content = urllib2.urlopen(request).read()
            #content = self.login().open(request).read()
            change_json = json.loads(content)
            change_json_list = change_json.get("list")
            for change_history in change_json_list:
                if change_history['status'] == 'failed':
                    continue
                else:
                    if(len(change_history.get("rebalancing_histories"))==0):
                        continue
                    history_dict = change_history.get("rebalancing_histories")[0]
                    update_time = int(history_dict['updated_at'])
                    if update_time > yesterday_time:
                        change_str = history_dict['stock_name']+" "+str(history_dict['weight'])+"->"+str(history_dict['target_weight'])
                        hold_change_tuple.append(change_str)
            if single_info not in HoldChangeByProfit.hold_change_map:
                HoldChangeByProfit.hold_change_map[single_info] = str(hold_change_tuple)
                continue

            if str(HoldChangeByProfit.hold_change_map[single_info]) != str(hold_change_tuple):
                HoldChangeByProfit.hold_change_map[single_info] = str(hold_change_tuple)
                print "股票代码: "+single_info+" 持仓情况发生了变化，请注意!"
            #break
            # print content
            # soup = BeautifulSoup(content)
            # date_element = soup.findall("span", class_="date", limit=1)
    def login(self):
        session = requests.Session()
        login_url = "http://xueqiu.com/user/login"
        telephone = '18030659951'
        password = '140E2E1313B1910CF086B4A75D3DC05B'
        data = {'telephone':'18030659951','password':'140E2E1313B1910CF086B4A75D3DC05B','username':"","areacode":"86","remeber_me":"1"}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',\
                   'Host':"xueqiu.com",'Cookie':'s=v2x115hqe7; xq_a_token=ec225cc39134e9d7f331b34986471ab8a38b97c4; \
                   xq_r_token=72976e9c8f5ac083b294f89b658188b16f43bdb9',\
                   'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8"\
                   ,'Referer':"http://xueqiu.com/4830787364"}
        r = session.post(login_url, data=data, headers=headers)
        #HoldChangeByProfit.cookies = r.headers['cookies']
        HoldChangeByProfit.cookies = r.cookies
        print r.text
        return session


if __name__ == '__main__':
    import sys
    reload(sys)
    #hold.get_Hold_Page()
    # hold.get_single_hold_url()
    # while(True):
    #     hold.get_all_hold_page_content()
    hold = HoldChangeByProfit()
    hold.login()
    #hold.get_Hold_Page()
    #hold.get_single_hold_url()
    # hold.get_all_hold_page_content()