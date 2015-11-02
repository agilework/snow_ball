__author__ = 'admin'
__author__ = 'admin'
#-*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import json
class DataForDay:
    peopel_url={}
    def get_people_with_ten_page(self):
        headers = {#'X-Requested-With': 'XMLHttpRequest',
           #'Referer': 'http://xueqiu.com/p/ZH010389',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
           #'Host': 'xueqiu.com',
           #'Connection':'keep-alive',
           #'Accept':'*/*',
           'cookie':'s=by4123qk8x; xq_a_token=5f6288e0798e3e42f8a32863f2c994554a3712b6; xq_r_token=eca50f274592156d4d555cb566506a75062be426;Hm_lvt_1db88642e346389874251b5a1eded6e3=1444664452'}
        page_count = 10
        url_array =[]
        for i in range(1,5):
            url = "http://xueqiu.com/cubes/discover/rank/cube/list.json?category=10&count="+str(page_count*i)+"&market=cn"
            url_array.append(url)
        for url in url_array:
            print url
            req = urllib2.Request(url, headers=headers)
            content = urllib2.urlopen(req).read()
            #soup = BeautifulSoup(content)
            content_json = json.loads(content)
            json_list = content_json["list"]
            for json_obect in json_list:
                if "name" in json_obect:
                    DataForDay.peopel_url[json_obect["name"]]=json_obect["symbol"]
        print DataForDay.peopel_url

    def get_every_people_get(self):
        url_prefix = "http://xueqiu.com/p/"
        pass

if __name__ == '__main__':
    day = DataForDay();
    day.get_people_with_ten_page()