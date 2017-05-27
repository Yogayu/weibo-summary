#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
# 存储摘要性能值

from subprocess import call

# call(['python', 'Random.py'])
# call(['python', 'Hybrid-TFIDF.py'])
# call(['python', 'MostRecent.py'])
# call(['python', 'TFIDF.py'])
# call(['python', 'TextRank.py'])
call(['rm', '.DS_Store'],
     cwd='/Users/apple/scrapingEnv/weibo-summary/ROUGE/test-summarization/system')
call('java -jar rouge2.0_0.2.jar', shell=True,
     cwd='/Users/apple/scrapingEnv/weibo-summary/ROUGE')
call(['python processResult.py'], shell=True,
     cwd='/Users/apple/scrapingEnv/weibo-summary/ROUGE')
