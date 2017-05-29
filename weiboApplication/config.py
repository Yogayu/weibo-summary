#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

import sys, os

# 设置编码格式
reload(sys)
sys.setdefaultencoding('utf-8')

def get_base_dir():
    return os.path.abspath(os.path.dirname(__file__))