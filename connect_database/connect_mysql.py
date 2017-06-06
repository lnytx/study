#-*-coding:utf-8-*-
'''
Created on 2017年3月27日

@author: admin
'''
import mysql.connector #MySQL Connectors




def connect():
    config={'host':'127.0.0.1',
                'user':'root',
                'password':'root',
                'port':3306,
                'database':'get_sysinfo',
                'charset':'utf8'
            }
    try:
        conn=mysql.connector.connect(**config)
        return conn
        print("conn is success!")
    except mysql.connector.Error as e:
        print("conn is fails{}".format(e))
#执行SQL，提供表名与sql语句
def execute(sql):
    try:
        conn=connect()
        cursor=conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print("sql %s, is success" % sql)
    except mysql.connector.Error as e:
        print("sql %s, is faild".format(e) % sql)
        conn.rollback()
    conn.close()        

def delete_table(table_name,ip):
    sql_delete = "delete from %s where ip='%s'" % (table_name,ip)
    try:
        conn=connect()
        cursor=conn.cursor()
        cursor.execute(sql_delete)
        conn.commit()
    except mysql.connector.Error as e:
        print("insert cursor is faild".format(e))
        conn.rollback()
    conn.close()  

def select_table(table_name,ip):
    count="select ip from %s where ip= '%s' " % (table_name,ip)
    result=[]
    try:
        conn=connect()
        cursor=conn.cursor()
        cursor.execute(count)
        result = cursor.fetchall()#queryset返回列表
        if len(result)==0:
            return False
        else:
            return True
    except mysql.connector.Error as e:
        print("select count is faild".format(e))
    conn.close()
def insert_cpuinfo(list_args):
    if (len(list_args)>8):
        return
    print("list_args",list_args)
    sql_insert = "INSERT INTO cpuinfo(ip,\
       hostname, scputimes, dpc, idle,interrupt,system,user)\
       VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" %\
       (list_args[0], list_args[1], list_args[2], list_args[3], list_args[4],list_args[5],list_args[6],list_args[7])
    print("sql_insert",sql_insert)
    try:
        conn=connect()
        cursor=conn.cursor()
        cursor.execute(sql_insert)
        conn.commit()
    except mysql.connector.Error as e:
        print("insert cursor is faild".format(e))
        conn.rollback()
    conn.close()        
def update_cpuinfo(ip,list_args):
    if (len(list_args)>8):
        return
    print("list_args",list_args)
    sql_insert = "update cpuinfo\
       set hostname=%s, scputimes=%s, dpc=%s, idle=%s,interrupt=%s,system=%s,user=%s\
       where ip=%s"\
       %(list_args[1], list_args[2], list_args[3], list_args[4], list_args[5],list_args[6],list_args[7],ip) 
    print("sql_insert",sql_insert)
    try:
        conn=connect()
        cursor=conn.cursor()
        cursor.execute(sql_insert)
        conn.commit()
    except mysql.connector.Error as e:
        print("update cursor is faild".format(e))  
        conn.rollback()
    conn.close()
    
    
