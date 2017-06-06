from _csv import Error
from _pickle import loads
import json
from multiprocessing import cpu_count

from django.http.response import HttpResponse
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import mysql.connector

from connect_database.connect_mysql import connect, execute, select_table,\
    delete_table


# Create your views here.
def home(request):
    jstr=[]
    scputimes=[]
    cpuinfo=dict()
    system_info=dict()
    try:
        if request.method=='POST':
            #jstr = request.body.decode('unicode-escape')#这是解析成未序列化之前的串
            jstr = request.body.decode("utf-8")
            print("type",type(jstr))
            #反序列化，将json转化成dict类型
            data = json.loads(jstr)
            #ip=jstr.ip_hostname.ip
            print("j",data)
            ip=data['IP_hostname']['ip']
            hostname=data['IP_hostname']['hostname']
            #获取system_info表的字段
            system_info['system_info'] = {
            'ip': ip, 
            'hostname': hostname,
            'physicalCPU': data['cpu_count']['物理个数'], 
            'logicalCPU': data['cpu_count']['逻辑个数'],
            'platform':data['cpu_count']['platform']
            }
            #判断已存在的表中是否已经存在相同IP的值，如果有，则为true,对应的sql为更新，如果没有则为false对应的sql为insert
            cpuinfo_flag=select_table('cpuinfo', ip)
            ip_hostname_flag=select_table('ip_hostname', ip)
            
    #针对windows系统代码
            if data['cpu_count']['platform']=='Windows':
                #获取所有CPU表的字段
                for items in data:
                    if items[0:-1]=='scputimes' or items[0:-2]=='scputimes':
                        scputimes.append(items)
                for i in range(len(scputimes)):
                    cpuinfo[scputimes[i]] = {
                        'user': data[scputimes[i]]['user'], 
                        'system': data[scputimes[i]]['system'],
                        'idle': data[scputimes[i]]['idle'], 
                        'interrupt': data[scputimes[i]]['interrupt'],
                        'dpc':data[scputimes[i]]['dpc']
                        }
                    #拼接cpu相关的sql语句
                    sql_cpuinfo = "INSERT INTO cpuinfo \
                            (ip,hostname, scputimes, dpc,idle,interrupt,system,user)\
                            VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s')"  \
                            %(ip,hostname,scputimes[i],data[scputimes[i]]['dpc'],\
                            data[scputimes[i]]['idle'], data[scputimes[i]]['interrupt'],\
                            data[scputimes[i]]['system'],data[scputimes[i]]['user'])
                    if cpuinfo_flag:#为真则表明该表中已经有相同的IP的信息，于是执行update语句
                        delete_table('cpuinfo',ip)#先删除再新增
                        execute(sql_cpuinfo)
                    else:
                        print("直接执行windows insert")
                        print("true or false",cpuinfo_flag)
                        execute(sql_cpuinfo)#执行sql，这是一个方法
                cpuinfo['system']={
                    'ip': ip,
                    'hostname': hostname
                }
                #处理ip_hostname表
                if ip_hostname_flag:#如果表中有相同IP的，就update
                    #先删除原来对应的IP记录，然后再插入
                    delete_table('ip_hostname',ip)
                    sql_ip_hostname = "update ip_hostname\
                    set hostname='%s', physicalCPU=%s, logicalCPU=%s,platform='%s' \
                    where ip='%s'" \
                    %(system_info['system_info']['hostname'], system_info['system_info']['physicalCPU'],\
                      system_info['system_info']['logicalCPU'],system_info['system_info']['platform'],ip)
                    #for k,v in cpuinfo.items():

                else:
                    sql_ip_hostname = "INSERT INTO ip_hostname(ip,\
                    hostname, physicalCPU, logicalCPU,platform)\
                    VALUES ('%s', '%s', '%s', '%s','%s')"  \
                    %(system_info['system_info']['ip'],\
                    system_info['system_info']['hostname'],\
                    system_info['system_info']['physicalCPU'],\
                    system_info['system_info']['logicalCPU'],\
                    system_info['system_info']['platform'])
                execute(sql_ip_hostname)  
#                         "
            #针对linux系统的代码
            #处理cpuinfo表的sql
            elif data['cpu_count']['platform']=='Linux':
                for items in data:
                    if items[0:-1]=='scputimes' or items[0:-2]=='scputimes':
                        scputimes.append(items)
                for i in range(len(scputimes)):
                    cpuinfo[scputimes[i]] = {
                        'user': data[scputimes[i]]['user'], 
                        'system': data[scputimes[i]]['system'],
                        'idle': data[scputimes[i]]['idle'], 
                        'iowait': data[scputimes[i]]['iowait'],
                        'guest':data[scputimes[i]]['guest'],
                        'irq':data[scputimes[i]]['irq'],
                        'softirq':data[scputimes[i]]['softirq'],
                        'steal':data[scputimes[i]]['steal'],
                        'nice':data[scputimes[i]]['nice']
                        }
                    #创建linux下的cpuinfo表的sql
                    sql_cpuinfo = "INSERT INTO cpuinfo \
                            (ip,hostname,scputimes,user, system,idle,iowait,guest,irq,softirq,steal,nice)\
                            VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                            %(ip,hostname,scputimes[i],data[scputimes[i]]['user'],data[scputimes[i]]['system'],\
                            data[scputimes[i]]['idle'], data[scputimes[i]]['iowait'],data[scputimes[i]]['guest'],\
                            data[scputimes[i]]['irq'],data[scputimes[i]]['softirq'],data[scputimes[i]]['steal'],data[scputimes[i]]['nice'])
                    if cpuinfo_flag:#为真则表明该表中已经有相同的IP的信息，于是执行update语句
                        delete_table('cpuinfo',ip)#先删除再新增
                        execute(sql_cpuinfo)
                    else:
                        execute(sql_cpuinfo)#执行sql，这是一个方法
                cpuinfo['ip']=ip
                cpuinfo['hostname']=hostname
                #print("cpuinfo",cpuinfo)
                #处理ip_hostname表
                sql_ip_hostname = "INSERT INTO ip_hostname(ip,\
                    hostname, physicalCPU, logicalCPU,platform)\
                    VALUES ('%s', '%s', '%s', '%s','%s')"  \
                    %(system_info['system_info']['ip'],\
                    system_info['system_info']['hostname'],\
                    system_info['system_info']['physicalCPU'],\
                    system_info['system_info']['logicalCPU'],\
                    system_info['system_info']['platform'])
                if ip_hostname_flag:#如果表中有相同IP的，就update
                    delete_table('ip_hostname', ip)
                    execute(sql_ip_hostname)
#                     sql_ip_hostname = "update ip_hostname\
#                     set hostname='%s', physicalCPU='%s', logicalCPU='%s',platform='%s' \
#                     where ip='%s'" \
#                     %(system_info['system_info']['hostname'], system_info['system_info']['physicalCPU'],\
#                       system_info['system_info']['logicalCPU'],system_info['system_info']['platform'],ip)
    
                else:
                    execute(sql_ip_hostname)
            #针对其他系统的代码，简单的记录几个字段
            else:
                for items in data:
                    if items[0:-1]=='scputimes' or items[0:-2]=='scputimes':
                        scputimes.append(items)
                for i in range(len(scputimes)):
                    cpuinfo[scputimes[i]] = {
                        'user': data[scputimes[i]]['user'], 
                        'system': data[scputimes[i]]['system']
                        }
                    #创建linux下的cpuinfo表的sql
                    sql_cpuinfo = "INSERT INTO cpuinfo \
                            (ip,hostname,scputimes,user, system)\
                            VALUES ('%s', '%s', '%s', '%s','%s')" \
                            %(ip,hostname,scputimes[i],data[scputimes[i]]['user'],data[scputimes[i]]['system'])
                    if cpuinfo_flag:#为真则表明该表中已经有相同的IP的信息，于是执行update语句
                        delete_table('cpuinfo',ip)#先删除再新增
                        execute(sql_cpuinfo)
                    else:
                        execute(sql_cpuinfo)#执行sql，这是一个方法
                cpuinfo['ip']=ip
                cpuinfo['hostname']=hostname
                #print("cpuinfo",cpuinfo)
                #处理ip_hostname表
                print("Ture or false",select_table('ip_hostname',ip))
                if ip_hostname_flag:#如果表中有相同IP的，就update
                    sql_ip_hostname = "update ip_hostname\
                    set hostname='%s', physicalCPU=%s, logicalCPU=%s,platform='%s' \
                    where ip='%s'" \
                    %(system_info['system_info']['hostname'], system_info['system_info']['physicalCPU'],\
                      system_info['system_info']['logicalCPU'],system_info['system_info']['platform'],ip)
                else:
                    sql_ip_hostname = "INSERT INTO ip_hostname(ip,\
                    hostname, physicalCPU, logicalCPU,platform)\
                    VALUES ('%s', '%s', '%s', '%s','%s')"  \
                    %(system_info['system_info']['ip'],\
                    system_info['system_info']['hostname'],\
                    system_info['system_info']['physicalCPU'],\
                    system_info['system_info']['logicalCPU'],\
                    system_info['system_info']['platform'])
                execute(sql_ip_hostname)
            print("sql_ip_hostname",sql_ip_hostname)
            #print("jstr",jstr)
        return render(request, 'home.html',{'jstr':jstr})
    except Error as e:
        import sys
        print("except",str(e))
        return HttpResponse(str(e), 'home.html')

