'''
Created on 2017年6月1日

@author: ning.lin
'''
import socket


str='\\u4ee5\\u592a\\u7f51'
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print("hostname",hostname)
print("ip",ip)
