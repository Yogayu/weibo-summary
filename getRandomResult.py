#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
# Random得到的值存在波动
# 所以，多次运行Random算法得到摘要
# 并取得摘要性能值之后，计算其平均值

from subprocess import call

for i in xrange(0,100):
    call(['python', 'Random.py'])
    call(['rm', '.DS_Store'],
         cwd='/Users/apple/scrapingEnv/weibo-summary/ROUGE/test-summarization/system')
    call('java -jar rouge2.0_0.2.jar', shell=True,
         cwd='/Users/apple/scrapingEnv/weibo-summary/ROUGE')
    call(['python processResult.py'], shell=True,
         cwd='/Users/apple/scrapingEnv/weibo-summary/ROUGE')
