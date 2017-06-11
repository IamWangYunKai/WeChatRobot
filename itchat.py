# -*- coding: utf-8 -*-

import itchat,time
from itchat.content import *

import urllib.request
import urllib.parse
import json

'''
##自动回复的功能
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg['Text']
'''

wea='***'

class ZuiMei():
    def __init__(self):
        self.url = 'http://www.zuimeitianqi.com/zuimei/queryWeather'
        self.headers = {}
        self.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        # 部分城市的id信息
        self.cities = {}
        self.cities['成都'] = '01012703'
        self.cities['杭州'] = '01013401'
        self.cities['深圳'] = '01010715'
        self.cities['广州'] = '01010704'
        self.cities['上海'] = '01012601'
        self.cities['北京'] = '01010101'
        # Form Data
        self.data = {}
        self.city = '杭州'
        
    
    def query(self,city='杭州'):
        global wea
        if city not in self.cities:
            print('暂时不支持当前城市')
            return
        self.city = city
        data = urllib.parse.urlencode({'cityCode':self.cities[self.city]}).encode('utf-8')
        req = urllib.request.Request(self.url,data,self.headers)
        response = urllib.request.urlopen(req)
        
        html = response.read().decode('utf-8')
        # 解析json数据并打印结果
        
        target = json.loads(html)
        high_temp = target['data'][0]['actual']['high']
        low_temp = target['data'][0]['actual']['low']
        current_temp = target['data'][0]['actual']['tmp']
        today_hum = target['data'][0]['actual']['hum']
        air_desc = target['data'][0]['actual']['desc']
        # 上海 6~-2°C 现在温度 1°C 湿度：53 空气质量不好，注意防霾。
        wea=str(self.city)+'： '+str(low_temp)+'~'+str(high_temp)+'°C\n现在温度：'+str(current_temp)+'°C\n湿度：'+str(today_hum)+'%\n'+str(air_desc)
        #wea=print('%s: %s~%s°C 现在温度 %s°C 湿度：%s%% %s'%(self.city,low_temp,high_temp,current_temp,today_hum,air_desc))

#Still not working!!!
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['Text'].find('噫') != -1:
      itchat.send(('噫'), msg['FromUserName'])
      
    elif msg['Text'].find('天气预报') != -1:
        zuimei = ZuiMei()
        zuimei.query('杭州')
        itchat.send((wea), msg['FromUserName'])
        
@itchat.msg_register([TEXT])
def text_reply(msg):
    if msg['Text'].find('噫') != -1:
      itchat.send(('噫'), msg['FromUserName'])
      
    elif msg['Text'].find('天气预报') != -1:
        zuimei = ZuiMei()
        zuimei.query('杭州')
        itchat.send((wea), msg['FromUserName'])
      
@itchat.msg_register([PICTURE, RECORDING, VIDEO, SHARING])
def other_reply(msg):
    itchat.send(('[捂脸]'), msg['FromUserName'])

    
#@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
#def text_reply(msg):
#    itchat.send('%s: %s'%(msg['Type'],msg['Text']),msg['FromUserName'])

#@itchat.msg_register([PICTURE,RECORDING,ATTACHMENT,VIDEO])
#def download_files(msg):
#    msg['Text'](msg['FileName'])
#    return '@%s@%s'%({'Picture':'img','Video':'vid'}.get(msg['Type'],'fil'),msg['FileName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])# 该操作将自动将好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!',msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT,isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s '%(msg['ActualNickName'],msg['Content']),msg['FromUserName'])


itchat.auto_login(hotReload=True)

#向文件助手发送消息
itchat.send('Hello File Helper',toUserName='filehelper')

itchat.run()
