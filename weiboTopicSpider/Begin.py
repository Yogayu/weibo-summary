#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

from scrapy import cmdline

cmdline.execute("scrapy crawl weibo_topic_spider".split())
