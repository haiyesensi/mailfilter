#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-12-18 13:10:34
# Project: mailfilter

from pyspider.libs.base_handler import *
import re
import pymysql

match_rule = "^[a-zA-Z0-9_-]+((\.[a-zA-Z0-9_-]+)|([a-zA-Z0-9_-]+))@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        start_url = 'http://uoj.ac/ranklist?page='        
        page = 1
        page_end = 97
        while page <= page_end:
            url = start_url+str(page)
            self.crawl(url,callback=self.index_page)
            page += 1
            
        
#得到一个页面中所有的一百个用户名
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        user_url = 'http://uoj.ac/user/profile/'
        string = response.doc('td > span').text()  
        list = string.split(" ")
        for i in list:
            realuser_url = user_url+i
            print(realuser_url)            
            self.crawl(realuser_url, callback=self.getmail_page)

#得到每个用户资料页面下的邮箱
    def getmail_page(self,response):
        usermail = response.doc('body > div > div.uoj-content > div > div.panel-body > div.row > div.col-md-8.col-md-pull-4 > div > div:nth-child(2) > p').text()
        saveMysql(usermail)
        
                
def saveMysql(str):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='jwerrrer71a', db='spidertest')
    cursor = conn.cursor()
    sql = 'INSERT INTO mailfilter(mailaddress,status)VALUES (%s,%s)'
    if (re.match(match_rule, str) == None):
        cursor.execute(sql, (str, "n"))
    else:
        cursor.execute(sql, (str,""))
    conn.commit()
    cursor.close()
    conn.close()   
        
        