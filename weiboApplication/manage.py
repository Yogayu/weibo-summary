#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
from flask_script import Manager
from weiboModel import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

manager = Manager(app)

# def setEvn():
    # manager.export FLASK_APP=hello.py
@manager.command
def add_weibo():
    print("weibo")
    # weibo = Weibo(u"#北京#", u"123", u"123中文", u"23", u"你好")
    weibo = Weibo(u"1234中文","45","12","3","2")
    weibo.add()

# @manager.command
# def delete_weibo():
#     weibos = show()
#     weibo = weibos[0]
#     weibo.delete()

@manager.command
def show():
    print get_all_summary('hhah')

    
@manager.command
def create_all_table():
    db.create_all()

if __name__ == '__main__':
    manager.run()