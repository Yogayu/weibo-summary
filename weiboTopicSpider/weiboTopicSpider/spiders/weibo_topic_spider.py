#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
import re
import datetime
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from weiboTopicSpider.items import WeibotopicspiderItem

class Spider(CrawlSpider):
    name = "weibo_topic_spider"
    host = "http://weibo.cn"
    allowed_domains = ["weibo.cn"]
    search_url = 'http://weibo.cn/search/mblog'
    max_page = 200
    keywords = ['%23%E4%B8%A4%E4%BC%9A%23']

    def start_requests(self):
        for keyword in self.keywords:
            url = '{url}?hideSearchFrame=&keyword={keyword}&sort=hot&page=1'.format(
                url=self.search_url, keyword=keyword)
            # url = 'http://7xle3b.com1.z0.glb.clouddn.com/mweibo.html'
            print(url)
        # yield Request(url, callback=self.parse_detail)
        yield Request(url,
                  meta = {
                      'dont_redirect': True,
                      'handle_httpstatus_list': [302]
                  },
                  callback= self.parse_detail)

    def parse_detail(self, response):
        if response.status == 302:
            print "30000222"
            print response.request.meta.get('handle_httpstatus_list')
            print "down"
            # url = "http://weibo.cn/search/mblog?hideSearchFrame=&keyword=%23%E4%B8%A4%E4%BC%9A%23&sort=hot&page=2"
            url = "http://passport.weibo.cn/sso/crossdomain?service=sinawap&display=0&ssosavestate=1526916246&url=http%3A%2F%2Fweibo.cn%2Fsearch%2Fmblog%3FhideSearchFrame%3D%26keyword%3D%2523%25E4%25B8%25A4%25E4%25BC%259A%2523%26sort%3Dhot%26page%3D2&ticket=ST-NTYzOTI1Nzk3Nw==-1495381682-gz-A56C75C6D9E9948F929198323ED2681E-1&retcode=0"
            yield Request(url,
                  meta = {
                      'dont_redirect': True,
                      'handle_httpstatus_list': [302]
                  },
                  callback= self.parse_detail)
        print "I'm on: %s with status %d" % (response.url, response.status)
        # print(response.text)
        # print(response.headers)
        """ 抓取微博数据 """
        print("Beign to Crawl")
        selector = Selector(response)
        tweets = selector.xpath('body/div[@class="c" and @id]')
        for tweet in tweets:
            tweetsItems = WeibotopicspiderItem()
            id = tweet.xpath('@id').extract_first()  # 微博ID
            content = tweet.xpath(
                'div/span[@class="ctt"]/text()').extract()  # 微博内容
            like = re.findall(u'\u8d5e\[(\d+)\]', tweet.extract())  # 点赞数
            transfer = re.findall(
                u'\u8f6c\u53d1\[(\d+)\]', tweet.extract())  # 转载数
            comment = re.findall(
                u'\u8bc4\u8bba\[(\d+)\]', tweet.extract())  # 评论数
            others = tweet.xpath(
                'div/span[@class="ct"]/text()').extract_first()  # 求时间和使用工具（手机或平台）

            tweetsItems["ID"] = id
            tweetsItems["_id"] = id
            if content:
                # tweetsItems["Content"] = content.strip(u"[\u4f4d\u7f6e]")  #
                # 去掉最后的"[位置]"
                tweetsItems["Content"] = content
            # if cooridinates:
            #     cooridinates = re.findall('center=([\d|.|,]+)', cooridinates)
            #     if cooridinates:
            #         tweetsItems["Co_oridinates"] = cooridinates[0]
            if like:
                tweetsItems["Like"] = int(like[0])
            if transfer:
                tweetsItems["Transfer"] = int(transfer[0])
            if comment:
                tweetsItems["Comment"] = int(comment[0])
            if others:
                others = others.split(u"\u6765\u81ea")
                tweetsItems["PubTime"] = others[0]
                if len(others) == 2:
                    tweetsItems["Tools"] = others[1]
            yield tweetsItems
            url_next = selector.xpath(
                u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
            if url_next:
                yield Request(url=self.host + url_next[0], callback=self.parse_detail)
