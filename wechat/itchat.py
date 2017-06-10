# -*- coding: utf-8 -*-

import itchat,time,re
from itchat.content import *

'''
##自动回复的功能
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg['Text']
'''

@itchat.msg_register([TEXT])
def text_reply(msg):
    match = re.search('年', msg['Text']).span()
    if match:
      itchat.send(('新年快乐！'), msg['FromUserName'])
      
@itchat.msg_register([PICTURE, RECORDING, VIDEO, SHARING])
def other_reply(msg):
    itchat.send(('鸡年大吉！'), msg['FromUserName'])

    
#@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
#def text_reply(msg):
#    itchat.send('%s: %s'%(msg['Type'],msg['Text']),msg['FromUserName'])

@itchat.msg_register([PICTURE,RECORDING,ATTACHMENT,VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s'%({'Picture':'img','Video':'vid'}.get(msg['Type'],'fil'),msg['FileName'])

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
itchat.send('Hello filehelper',toUserName='filehelper')

itchat.run()