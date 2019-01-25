import re
import csv
import lxml.html
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime

# 写入csv
def wcsv(html):
    # 模仿网站
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
        # 写入天气信息
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

# 生成城市对应url
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

# 可视化
def getplot():
    with open('weather.csv') as f:
        # 读文件
        reader = csv.reader(f)
        # 使用csv的next函数，将reader传给next，返回文件的下一行
        header_row = next(reader)
        header_row = next(reader)
        # 读取最高/最低温
        # 创建最高/最低温列表
        highs = []
        lows = []
        # 日期列表
        days = []
        # 遍历reader的余下的所有行（next读取了第一行，reader每次读取后将返回下一行）
        for row in reader:
            # 将字符串转换成数字
            high = int(row[2])
            low = int(row[3])
            day = int(row[0])
            highs.append(high)
            lows.append(low)
            days.append(day)

        # 绘制图形
        fig = plt.figure(dpi=128, figsize=(10, 6))
        # 显示中文字
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(days, highs, c='red', label='最高温')
        plt.plot(days, lows, c='blue', label="最低温")
        # 显示当前时间
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
        # 标题
        plt.title(nowTime+city_name+"天气频道最高/低温", fontsize=24)
        # x轴
        plt.xlabel('Day', fontsize=16)
        # y轴
        plt.ylabel("Temperature(℃)", fontsize=16)
        plt.tick_params(axis='both', which="major", labelsize=16)

        plt.legend()
        plt.show()


if __name__ == '__main__':
    city_name=input('请输入城市名：')
    html=get_url(city_name)
    wcsv(html)
    getplot()

