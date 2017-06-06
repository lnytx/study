'''
Created on 2017年5月31日

@author: ning.lin
'''
#!/usr/local/src/python/bin/python
#-*- coding:utf-8 -*-
import json
import logging
import platform
import socket
import sys

import psutil
import requests


def get_DistkInfo():
    #磁盘信息
    dic=dict()
    disk=psutil.disk_partitions()
    print("disk",disk)
#         #range(1,5,2) #代表从1到5，间隔2(不包含5)
#         for j in range(0,len(list_disk),6):
#             items.append(list_disk[j:j+6])
#磁盘信息 [sdiskpart(device='C:\\', mountpoint='C:\\', fstype='NTFS', opts='rw,fixed'), sdiskpart(device='D:\\', mountpoint='D:\\', fstype='NTFS', opts='rw,fixed')]
#     for items in disk:
#         dk.append(items)
#将disk这个list转换成dict，以方便json序列化
    for i in range(0,len(disk)):
        dic['sdiskpart'+str(i)] = {
        'device': disk[i].device, 
        'mountpoint': disk[i].mountpoint,
        'fstype': disk[i].fstype, 
        'opts': disk[i].opts,
        }
    return dic
def get_CpuInfo():
    dic=dict()
    cpu=psutil.cpu_times(percpu=True)
    if platform.system()=='Windows':
#[scputimes(user=200590.359375, system=305576.125, idle=1394456.0, interrupt=44782.984375, dpc=68005.796875), scputimes(user=218519.53125, system=178113.0, idle=1503989.625, interrupt=9030.15625, dpc=374.5625), scputimes(user=258630.609375, system=193022.0, idle=1448969.5, interrupt=1023.859375, dpc=41.375003814697266), scputimes(user=306111.15625, system=158958.625, idle=1435552.375, interrupt=824.140625, dpc=16.59375)]
        print("type",type(cpu),cpu)
        #查看CPU所有的信息
        #print("CPU所有信息",psutil.cpu_times())
        #cpu逻辑个数
        print("逻辑个数",psutil.cpu_count())
        #cpu物理个数
        print("物理个数",psutil.cpu_count(logical=False))
        for i in range(0,len(cpu)):
            dic['scputimes'+str(i)] = {
            'user': cpu[i].user, 
            'system': cpu[i].system,
            'idle': cpu[i].idle, 
            'interrupt': cpu[i].interrupt,
            'dpc':cpu[i].dpc
            }
        #这里每次都被覆盖了，所以只剩下scputimes4": {"逻辑个数": 4, "物理个数": 2}}
        dic['cpu_count']={
        '逻辑个数':psutil.cpu_count(),
        '物理个数':psutil.cpu_count(logical=False),
        'platform':platform.system()
        }
    elif platform.system()=='Linux':
        for i in range(0,len(cpu)):
            dic['scputimes'+str(i)] = {
            'user': cpu[i].user, 
            'system': cpu[i].system,
            'idle': cpu[i].idle, 
            'nice': cpu[i].nice,
            'iowait':cpu[i].iowait,
            'steal':cpu[i].steal,
            'guest':cpu[i].guest,
            'softirq':cpu[i].softirq,
            'irq':cpu[i].softirq
            }
        #这里每次都被覆盖了，所以只剩下scputimes4": {"逻辑个数": 4, "物理个数": 2}}
        dic['cpu_count']={
        '逻辑个数':psutil.cpu_count(),
        '物理个数':psutil.cpu_count(logical=False),
        'platform':platform.system()
        }
    else:
        for i in range(0,len(cpu)):
            dic['scputimes'+str(i)] = {
            'user': cpu[i].user, 
            'system': cpu[i].system
            }
        #这里每次都被覆盖了，所以只剩下scputimes4": {"逻辑个数": 4, "物理个数": 2}}
        dic['cpu_count']={
        '逻辑个数':psutil.cpu_count(),
        '物理个数':psutil.cpu_count(logical=False)
        }
    return dic
def get_MemInfo():
    list_mem=[]
    dic=dict()
##[svmem(total=7989456896, available=2227118080, percent=72.1, used=5762338816, free=2227118080), sswap(total=14703038464, used=8109694976, free=6593343488, percent=55.2, sin=0, sout=0)]
    #内存总信息
#     print("内存总信息",psutil.virtual_memory())
#     print("虚拟内存信息",psutil.swap_memory())
    mem=psutil.virtual_memory()
    sawp=psutil.swap_memory()
    dic['mem'] = {
    'total': mem.total, 
    'available': mem.available,
    'percent': mem.percent, 
    'used': mem.used,
    'free':mem.free
    }
    dic['sawp'] = {
    'total': sawp.total, 
    'used': sawp.used,
    'free': sawp.free, 
    'sin': sawp.sin,
    'sout':sawp.sout
    }
    return dic
def get_NetInfo():
    dic=dict()
    #print("网络信息",psutil.net_io_counters(pernic=True))
    s=psutil.net_io_counters(pernic=True)
    print("s",s)
###{'本地连接* 2': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0), 'Loopback Pseudo-Interface 1': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0), 'isatap.{3990D4E6-8745-4E23-95C4-7507658E79C9}': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0), 'WLAN': snetio(bytes_sent=1650562, bytes_recv=11610964, packets_sent=0, packets_recv=264, errin=0, errout=0, dropin=0, dropout=0), '以太网': snetio(bytes_sent=222706503, bytes_recv=1034659948, packets_sent=994032, packets_recv=980878, errin=0, errout=0, dropin=0, dropout=0), 'VMware Network Adapter VMnet1': snetio(bytes_sent=12801, bytes_recv=258, packets_sent=255, packets_recv=258, errin=0, errout=0, dropin=0, dropout=0), 'Reusable ISATAP Interface {22CF9987-060B-4C14-A959-6AFDB4D61AE0}': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0), 'isatap.Trendy-global.com': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0), 'VMware Network Adapter VMnet8': snetio(bytes_sent=52141, bytes_recv=11738, packets_sent=21560, packets_recv=11555, errin=0, errout=0, dropin=0, dropout=0), '蓝牙网络连接': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0)}
#
    for (k,v) in s.items():
        dic[k] = {
        'bytes_sent': v.bytes_sent, 
        'bytes_recv': v.bytes_recv,
        'packets_sent': v.packets_sent, 
        'packets_recv': v.packets_recv,
        'errin':v.errin,
        'errout':v.errout,
        'dropin':v.dropin,
        'dropout':v.dropout
    }
#         #for i in v:
#         #print("i",psutil._common.snetio.bytes_recv)
#         #获取网卡接收信息
#         print("sss",s.get(k).bytes_recv)
    return dic   
#     print(s["以太网"])
#     print(s["VMware Network Adapter VMnet8"].bytes_sent)
def get_IP():
    info = psutil.net_if_addrs()
    netcard_info = []
#     print(info)
    for k,v in info.items():
#         print("k",k)
#         print("v",v)
        for item in v:
#             print("type",type(item))
#             print("item",item)
#             print("item[0]",item[0])
#             print("item[1]",item[1])
#             print("item[0].value",item[0].value)
            #item[0]是dict而item[1]是list
            if item[0].value ==2 and not item[1]=='127.0.0.1':
                netcard_info.append((k,item[1]))
    return netcard_info
def get_Ip_Hostname():
    dic=dict()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    dic["IP_hostname"] = {
        'ip': ip, 
        'hostname': hostname,
    }
    return dic
def get_temperatures():
    if sys.platform == 'win32':
        t='this is Win;no sensors_temperatures module'
    else:
        t=psutil.sensors_temperatures(fahrenheit = False)
    return t
def pull_data(url,http_get_param=""):
    try:
        r = requests.get(url, params=http_get_param)
    except Exception as e:
        logging.error('connection django-cgi server error:'+str(e))
        sys.exit()
# def get_data():
#     data=[]
#     data.append(get_DistkInfo())
#     data.append(get_CpuInfo())
#     data.append(get_MemInfo())
#     data.append(get_NetInfo())
#     data.append(get_IP())
#     print("data",data)
#     return data
if __name__ == '__main__':
#     print ("磁盘信息",get_DistkInfo())
#     print ("CPU信息",get_CpuInfo())
#     print("内存信息",get_MemInfo())
    print("网络信息",get_Ip_Hostname())
#     print("IP信息",get_IP())
#     print("传感器信息",get_temperatures())
#     data = dict()
#     doc['server'] = socket.gethostname()
#     doc['date'] = datetime.now()
#     doc['disk_root'] = disk_root.free, 
#     doc['phymem'] = phymem.free


#     data.append(get_DistkInfo())
#     data.append(get_CpuInfo())
#     data.append(get_MemInfo())
#     data.append(get_NetInfo())
#     data.append(get_Ip_Hostname())
#     print("type",type(data))
#     for i in range(len(data)):
#         print("data",data[i])
    url='http://172.17.39.225:8000/home/'
#     print("data",data)
#     print("data[0]",data)
#     print("type",type(data))
    data1=get_Ip_Hostname()
    data2=get_DistkInfo()
    data3=get_CpuInfo()
    data4=get_MemInfo()
    #合并两个dict
    dataMerged1=dict(data1, **data2)
    dataMerger2=dict(data3,**data4)
    data=dict(dataMerged1,**dataMerger2)
    json_data= json.dumps(data,sort_keys=True)
    print("json_data",json_data)
    #这里是以unicode编码形式进行post的
    rq=requests.post(url,data=json_data)
