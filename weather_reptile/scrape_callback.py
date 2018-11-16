# -*- coding: utf-8 -*-

import csv
import re
from urllib.parse import urlparse
import lxml.html
from link_crawler import link_crawler
import json

#使用回调类而非回调函数以保持csv中write属性的状态
class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('weather.csv', 'w',newline=''))

        #天气 最高温/最低温 风力
        self.fields = ('天气','最高/低温','风力')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        #if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            td=tree.cssselect('p.wea')
            n=0
            for wea in td:
                row=[]
                row.append(tree.cssselect('p.wea')[n].text_content().strip('\n'))
                row.append(tree.cssselect('p.tem')[n].text_content().strip('\n'))
                row.append(tree.cssselect('p.win')[n].text_content().strip('\n'))
                n=n+1
                self.writer.writerow(row)

if __name__ == '__main__':
    link_crawler('http://www.weather.com.cn/weather/101020100.shtml', '/(index|view)', scrape_callback=ScrapeCallback())
