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
class HoldChangeByProfit:

    urls = []
    hold_map = {}
    single_html_content = []
    hold_change_map = {}
    final_sort_hold = {}
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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',\
                   'cookie':'s=v2x115hqe7; xq_a_token=ec225cc39134e9d7f331b34986471ab8a38b97c4; \
                   xq_r_token=72976e9c8f5ac083b294f89b658188b16f43bdb9'}
        if(len(HoldChangeByProfit.urls) == 0):
            print '没有最赚钱组合的urls!'
            exit(-1)
        for url in HoldChangeByProfit.urls:
            try:
                #opener = self.login()
                request = urllib2.Request(url,headers=headers)

                json_content = json.loads(urllib2.urlopen(request).read())
                #print opener.open(request).read()
                #json_content = json.loads(self.login().open(url).read())
                hold_list = json_content.get("list")
                for j in hold_list:
                    HoldChangeByProfit.hold_map[j['name']]=j['symbol']
            except Exception,e:
                print e
    #得到每个持股人的页面数据
    def get_all_hold_page_content(self):
        #得到昨天下午三点后的时间戳
        yesterday_time = int(time.mktime(time.strptime(str(date.today()-timedelta(days=1))+" 15:00","%Y-%m-%d %H:%M")))
        print yesterday_time
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',\
                   'cookie':'s=v2x115hqe7; xq_a_token=ec225cc39134e9d7f331b34986471ab8a38b97c4; \
                   xq_r_token=72976e9c8f5ac083b294f89b658188b16f43bdb9'}

        base_url_template = Template("http://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=$a&count=20&page=1")
        #print HoldChangeByProfit.hold_map.values()
        for single_info in HoldChangeByProfit.hold_map.values():
            print 'start to get ticket data page : '+single_info
            flag = True
            hold_change_tuple = []
            url = base_url_template.substitute(a=single_info)
            request = urllib2.Request(url, headers=headers)
            content = urllib2.urlopen(request).read()
            #content = self.login().open(request).read()
            change_json = json.loads(content)
            change_json_list = change_json.get("list")
            temp_map = {}
            for change_history in change_json_list:

                if change_history['status'] == 'failed':
                    continue
                else:
                    if(len(change_history.get("rebalancing_histories"))==0):
                        continue
                    history_dict_array = change_history.get("rebalancing_histories")
                    for o in history_dict_array:
                        update_time = int(o['updated_at'])
                    #update_time = int(history_dict['updated_at'])
                        if update_time > yesterday_time*1000:

                            hold_flag = o['stock_name']+'|'+o['stock_symbol']
                            if o['prev_weight'] == None:
                                o['prev_weight'] = 0
                            if o['weight'] == None:
                                o['weight'] = 0
                            if hold_flag not in temp_map and o['prev_weight']<o['weight'] and o['weight']>5:
                                temp_map[hold_flag]=1
                                print single_info+' have some done: '+o['stock_name']+'('+o['stock_symbol']+')'+" start from "+str(o['prev_weight'])+'% to '+str(o['weight'])+'%'
            for key in temp_map.keys():
                if key in HoldChangeByProfit.final_sort_hold:
                    HoldChangeByProfit.final_sort_hold[key]=HoldChangeByProfit.final_sort_hold[key]+1
                else:
                    HoldChangeByProfit.final_sort_hold[key]=1
                        #change_str = history_dict['stock_name']+" "+str(history_dict['weight'])+"->"+str(history_dict['target_weight'])
                        #hold_change_tuple.append(change_str)
            #if single_info not in HoldChangeByProfit.hold_change_map:
                #HoldChangeByProfit.hold_change_map[single_info] = str(hold_change_tuple)
                #continue

            #if str(HoldChangeByProfit.hold_change_map[single_info]) != str(hold_change_tuple):
                #HoldChangeByProfit.hold_change_map[single_info] = str(hold_change_tuple)
                #print "股票代码: "+single_info+" 持仓情况发生了变化，请注意!"
            #break
            # print content
            # soup = BeautifulSoup(content)
            # date_element = soup.findall("span", class_="date", limit=1)
        dict = sorted(HoldChangeByProfit.final_sort_hold.iteritems(), key=lambda d:d[1], reverse = True)
        print dict
    def login(self):
        login_url = "http://xueqiu.com/user/login"
        telephone = '18030659951'
        password = '140E2E1313B1910CF086B4A75D3DC05B'
        data = {'telephone':telephone,'password':password,'username':"","areacode":"86","remeber_me":"1"}
        post_data=urllib.urlencode(data)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0','Header':"xueqiu.com"}
        cookieJar=cookielib.CookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        req=urllib2.Request(login_url,post_data,headers)
        result = opener.open(req)
        print result.read()
        return opener


if __name__ == '__main__':
    import sys
    reload(sys)
    hold = HoldChangeByProfit()
    hold.get_Hold_Page()
    hold.get_single_hold_url()
    hold.get_all_hold_page_content()
    print HoldChangeByProfit.hold_change_map
