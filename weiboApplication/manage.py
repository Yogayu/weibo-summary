#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
from flask_script import Manager
from weiboModel import *

manager = Manager(app)


def create_all_table():
    db.create_all()


@manager.command
def add_weibo():
    print("weibo")
    # weibo = Weibo(u"#北京#", u"123", u"123中文", u"23", u"你好")
    weibo = Weibo("1234","45","12","3","2")
    weibo.add()

if __name__ == '__main__':
    manager.run()