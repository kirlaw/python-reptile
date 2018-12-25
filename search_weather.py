# coding=utf-8
import csv
import re
import lxml.html
import urllib.request
#为java代码调用python用
#import sys

#写入csv
def wcsv(html):
    #模仿网站
    headers = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    html = urllib.request.urlopen(html).read()

    # 使用newline=''避免生成csv文件两行间空一行
    with open('E:\Project\weather_reptile_app\weather.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # 日期 天气 最高温 最低温
        fields = ('日期', '天气', '最高温', '最低温')
        writer.writerow(fields)
        #写入天气信息
        tree = lxml.html.fromstring(html)
        n = 0
        while(n < 7):
            row = []
            row.append(re.findall('\d{1,2}',tree.cssselect('span.day-detail')[n].text_content().strip('\n'))[1])
            row.append(tree.cssselect('td.description')[n].text_content().strip('\n'))
            row.append(tree.cssselect('td.temp')[n].text_content().strip('\n').split('°')[0])
            row.append(tree.cssselect('td.temp')[n].text_content().strip('\n').split('°')[1])
            n = n + 1
            writer.writerow(row)

#生成城市对应url
def get_url(city_name):
    url = 'https://weather.com/zh-CN/weather/tenday/l/'
    with open('E:\Project\weather_reptile_app\全国各大城市天气代码表.csv', 'r') as fs:
        lines = fs.readlines()
        for line in lines:
            if (city_name in line):
                code = line.split(',')[1].strip()
                print(code)
                return url + code + ':1:CH'
    raise ValueError('invalid city name')

'''
if __name__ == '__main__'的意思是：当.py文件被直接运行时，
if __name__ == '__main__'之下的代码块将被运行；当.py文件以模块形式被
导入时，if __name__ == '__main__'之下的代码块不被运行。
'''
if __name__ == '__main__':
    #java调用时注释掉这一句
    city_name=input('请输入城市名：')
    #java调用时使用 html=get_url(sys.argv[1])
    html=get_url(city_name)
    wcsv(html)
