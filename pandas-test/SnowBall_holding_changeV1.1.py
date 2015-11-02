__author__ = 'admin'
#-*- coding: utf-8 -*-
#寻找某段时间内总体盈利排行中，每个人在当天的持股变化
from string import  Template
import time
import datetime
import re
from datetime import date,timedelta
import  cookielib
import urllib2
import urllib
import json
from bs4 import BeautifulSoup

class HoldChangeByProfit:

    #得到所有持股人的页面url
    def __init__(self):
        self.headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',\
                   'cookie':'s=v2x115hqe7; bid=05ab14d40fecee5cefa0829da7135df2_ig974xmb; Hm_lvt_1db88642e346389874251b5a1eded6e3=1444664452,1445928739; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1446099489; xq_a_token=6331f2f31003363f4b8dad068936a360d5b30d8a; xq_r_token=59ede7ffa672a75ec7cf4ca223ce0aa484fee05e; xqat=6331f2f31003363f4b8dad068936a360d5b30d8a; xq_is_login=1; u=4830787364; xq_token_expire=Mon%20Nov%2023%202015%2014%3A18%3A13%20GMT%2B0800%20(CST)'}
        self.urls = []
        self.hold_map = {}
        self.single_html_content = []
        self.hold_change_map = {}
        self.final_sort_hold = {}
        self.personLists = []
        #定义计算某只股票一共被持有了多少次
        self.single_hoding_times = {}
        #定义计算某个版本被持有了多少次
        self.bankuai_hoding_times = {}
        #减仓的数据
        self.hoding_reduce = []

    def get_Hold_Page(self):
        template = Template("http://xueqiu.com/cubes/discover/rank/cube/list.json?market=cn&sale_flag=0&stock_positions=0&sort=best_benefit&category=12&profit=annualized_gain_rate&page=$a&count=20")
        #我默认是取的三页的数据，可以修改的
        base_page = range(1,18)
        for i in base_page:
            page = int(i)
            self.urls.append(template.substitute(a=str(page)))
    #得到单个持股人的信息
    def get_single_hold_url(self):
        if(len(self.urls) == 0):
            print '没有最赚钱组合的urls!'
            exit(-1)
        for url in self.urls:
            try:
                request = urllib2.Request(url,headers=self.headers)
                json_content = json.loads(urllib2.urlopen(request).read())
                hold_list = json_content.get("list")
                for j in hold_list:
                    #self.hold_map[j['name']]=j['symbol']
                    person = Single_Person_Data()
                    person.setPersonName(j['name'])
                    person.setDescription(j['symbol'])
                    #self.get_person_holding_info(person)
                    self.personLists.append(person)
            except Exception,e:
                print e
    #得到每个人的信息（比如上蹿下跳之类的）
    def get_person_holding_info(self):
        url_base = Template("http://xueqiu.com/p/$a")
        for person in self.personLists:
            #print 'person %s to start ' % person.getDescription()
            symbol = person.getDescription()
            url = url_base.substitute(a=symbol)
            request = urllib2.Request(url, headers=self.headers)
            page_info = urllib2.urlopen(request).read()
            soup = BeautifulSoup(page_info,"html.parser")
            #print len(soup.find_all("div", class_="cube-style"))
            info_element = soup.find_all("div", class_="cube-style")[0]
            person.setPersonInfo(info_element.get_text())
            #得到每个人的现金持有率
            segments = soup.find_all('span', class_='segment-weight weight')
            #print segments[-1]
            cash_percent = float(segments[-1].get_text().replace('%',''))
            person.setCashPercent(cash_percent)
            #self.personLists.append(person)
            #print info_element.get_text()
            self.count_holdings_time(page_info)

    #得到每个历史调仓的页面数据
    def get_all_hold_page_content(self):
        #得到昨天下午三点后的时间戳
        yesterday_time = int(time.mktime(time.strptime(str(date.today()-timedelta(days=1))+" 15:00","%Y-%m-%d %H:%M")))
        base_url_template = Template("http://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=$a&count=20&page=1")
        for person in self.personLists:
            person_description = person.getDescription()
            print 'start to get ticket data page : '+person_description
            url = base_url_template.substitute(a=person_description)
            request = urllib2.Request(url, headers=self.headers)
            content = urllib2.urlopen(request).read()
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
                        if update_time > yesterday_time*1000:
                            hold_flag = o['stock_name']+'|'+o['stock_symbol']
                            #print hold_flag
                            if o['prev_weight_adjusted'] == None:
                                o['prev_weight_adjusted'] = 0
                            if o['target_weight'] == None:
                                o['target_weight'] = 0
                            if hold_flag not in temp_map and o['prev_weight_adjusted']<o['target_weight'] and o['target_weight']>5:
                                temp_map[hold_flag]=1
                                #print person.getDescription()+' have some done: '+o['stock_name']+'('+o['stock_symbol']+')'+" start from "+str(o['prev_weight'])+'% to '+str(o['weight'])+'%'
                            if o['target_weight']<o['prev_weight_adjusted']:
                                s = u'减仓个人: '+person.getDescription()+u" 减仓 "+o['stock_name']+u" 从 "+str(o['prev_weight_adjusted'])+u"% 到"+str(o['target_weight'])+"%"
                                self.hoding_reduce.append(s)
                                #self.hoding_reduce[]
            person.setChangeHoldingMap(temp_map)
            for key in temp_map.keys():
                if key in self.final_sort_hold:
                    self.final_sort_hold[key]=self.final_sort_hold[key]+1
                else:
                    self.final_sort_hold[key]=1
        dict_c = sorted(self.final_sort_hold.iteritems(), key=lambda d:d[1], reverse = True)
        #print dict_c

    #处理每个人的历史数据
    def handler_history_data(self,history_array):
        pass
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
    def count_money_total(self):
        count = 0.0
        for person in self.personLists:
            count = count + person.getCashPercent()
        return count/len(self.personLists)
    #查看所有持股人的某支股票一共被持了多少次和版本被持有了多少次
    def count_holdings_time(self, html_content):
        pattern = re.compile("(\"holdings\":\[.*?\])")
        groups = re.search(pattern, html_content)
        old_json = '{'+groups.group(1)+'}'
        hold_dict = json.loads(old_json)
        stock_list = hold_dict.get("holdings")
        temp_dict = {}
        for stock in stock_list:
            stock_name = stock.get('stock_name')
            stock_symbol = stock.get('stock_symbol')
            segment_name = stock.get('segment_name')
            if segment_name not in temp_dict:
                if segment_name in self.bankuai_hoding_times:
                    self.bankuai_hoding_times[segment_name] = self.bankuai_hoding_times[segment_name]+1
                else:
                    self.bankuai_hoding_times[segment_name] = 1
                temp_dict[segment_name]=1

            key = stock_name+'|'+stock_symbol
            if key in self.single_hoding_times:
                self.single_hoding_times[key] = self.single_hoding_times[key]+1
            else:
                self.single_hoding_times[key] = 1

class Single_Person_Data:

    def setDescription(self, description):
        self.description = description

    def setChangeHoldingMap(self, ChangeHoldingMap):
        self.changeHoldingMap = ChangeHoldingMap

    def setPersonName(self, personName):
        self.personName = personName

    def setPersonInfo(self, personInfo):
        self.personInfo = personInfo

    def getDescription(self):
        return self.description
    def getPersonName(self):
        return self.personName
    def getPersonInfo(self):
        return self.personInfo
    def setCashPercent(self, cashPercent):
        self.cashPercent =cashPercent
    def getCashPercent(self):
        return self.cashPercent

if __name__ == '__main__':
    import sys
    reload(sys)
    hold = HoldChangeByProfit()
    hold.get_Hold_Page()
    hold.get_single_hold_url()
    hold.get_person_holding_info()
    print u'某只个股被多少人持有:'+json.dumps(sorted(hold.single_hoding_times.iteritems(),key=lambda d:d[1],reverse = True),encoding='utf-8',ensure_ascii=False)
    print u'某个板块被多少人持有:'+json.dumps(sorted(hold.bankuai_hoding_times.iteritems(),key=lambda d:d[1],reverse = True),encoding='utf-8',ensure_ascii=False)
    print u'现金持有比率'+str(float(hold.count_money_total()/100))
    hold.get_all_hold_page_content()


    print u'某只股票持仓的变化次数: '+json.dumps(sorted(hold.final_sort_hold.iteritems(),key=lambda d:d[1],reverse=True),encoding='utf-8',ensure_ascii=False)
    print str(hold.hoding_reduce).decode('unicode-escape').encode('utf-8')
