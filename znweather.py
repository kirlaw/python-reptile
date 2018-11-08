import lxml.html
import urllib.request

url = 'http://www.weather.com.cn/weather/101020100.shtml'
headers = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
html = urllib.request.urlopen(url).read()
tree = lxml.html.fromstring(html)
#[0]当天 [1]明天 ..依次7天
td = tree.cssselect('p.tem')[1]
wea=td.text_content()
print(wea)

