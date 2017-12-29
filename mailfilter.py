#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-12-21 19:57:48
# Project: uoj

from pyspider.libs.base_handler import *
import re


def validemail(e):
    if len(e)>= 5:
        if re.match("^[a-zA-Z0-9_-]+((\.[a-zA-Z0-9_-]+)|([a-zA-Z0-9_-]+))@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$",e) !=None:
            return e
    return False

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
        usernames = response.doc('td > span').text().split(" ")
        for username in usernames:
            url = user_url + username      
            self.crawl(url, save={'name': username}, callback=self.getmail_page)

#得到每个用户资料页面下的邮箱,Rating数量,AC数量
    def getmail_page(self,response):
        mail = response.doc('body > div > div.uoj-content > div > div.panel-body > div.row > div.col-md-8.col-md-pull-4 > div > div:nth-child(2) > p').text()
        rating_count = response.doc('.list-group-item-text > strong').text()
        AC_count = response.doc('body > div.container.theme-showcase > div.uoj-content > div > div.panel-body > div.list-group > div:nth-child(2) > h4').text()
        AC_count = re.search('[0-9]+',AC_count).group()
        #合法邮箱用pyspider自带数据库储存
        if validemail(mail):
            return {
                'name': response.save['name'],
                'email': mail,
                'rating': rating_count,
                'AC_count': AC_count
            }   