'''
Created on 2017年6月1日

@author: ning.lin
'''
import array
import socket

from bs4 import BeautifulSoup
import requests


# str='\\u4ee5\\u592a\\u7f51'
# hostname = socket.gethostname()
# ip = socket.gethostbyname(hostname)
# print("hostname",hostname)
# print("ip",ip)
# 
# t=[1,2,3,...,4]
# t.append(t)
# print("t",t)
# numbers = ' '.join('asf') # 数字
# print("numbers",numbers)
url = 'http://www.baidu.com'

source = requests.get(url, headers={'Accept-Encoding': 'gzip, deflate'}).text
html = BeautifulSoup(source, 'lxml')
picture_url_list = html.find_all('div')
print(picture_url_list)

# r = requests.post(url)
# print(r.headers)
# #print (r.text)