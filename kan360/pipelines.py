# -*- coding: utf-8 -*-
import mysql.connector
from kan360.managedata import formatProName
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Kan360Pipeline(object):
    
    user = 'root'
    password = 'lacom159753'
    database = 'smarthome'
    
    def __init__(self):
        self.conn = mysql.connector.connect(user=self.user, password=self.password, database=self.database, use_unicode=True)
        self.cursor = self.conn.cursor()
    
    #将记录插入数据库方法
    def process_item(self, item):
        try:
            self.conn = mysql.connector.connect(user=self.user, password=self.password, database=self.database, use_unicode=True)
            self.cursor = self.conn.cursor()
            insertSql = 'insert into program(name, zhuyan) values (%s, %s);'
            #将记录，插入数据库
            self.cursor.execute(insertSql, [item['name'], item['zhuyan']])
            self.conn.commit()
        except mysql.connector.Error as e:
            print('query error!{}'.format(e))
        finally:
            self.close_db()

    #查询数据库是否由此记录
    def search(self, proName):
        num = 0
        try:
            self.conn = mysql.connector.connect(user=self.user, password=self.password, database=self.database, use_unicode=True)
            self.cursor = self.conn.cursor()
            querySql = "select name, zhuyan from program where name = %s"
            self.cursor.execute(querySql, [proName, ])
            self.cursor.fetchall()
            num = self.cursor.rowcount
        except mysql.connector.Error as e:
            print('query error!{}'.format(e))
        finally:
            self.close_db()
        return num

    #关闭数据库相关资源
    def close_db(self):
        self.cursor.close()
        self.conn.close()

