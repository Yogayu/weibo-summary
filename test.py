#! /usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

documents = (
# "The sky is blue",
# "The sun is bright",
# "The sun in the sky is bright",
# "We can see the shining sun, the bright sun"
u"#一带一路#【微视频：#世界舞台上的习近平#】出访26次，超过160天，平均每年有1个月以上的时间是用于出访。杭州G20峰会期间平均一天会见6位领导人，有时一天仅睡4小时……四年多来，无论出国访问还是主场外交，超紧凑行程、满负荷运转是习近平工作的常态。L人民日报的秒拍视频",
u"【#一带一路#广告片首发，《WE》来了！】泰国的芒果，西班牙的弗拉明戈，哈萨克斯坦的迪玛希，阿根廷的梅西……祖国是啥模样？8个国家的大学生给出了自己的答案↓↓来，一个词形容祖国，你第一个想到的是____？熊猫？高铁？辣条？ L人民日报的秒拍视频",
u"#一带一路# 图文并茂讲述陆上丝绸之路的三十三处世界遗产。除了大雁塔小雁塔，你去过几处了？  推荐关注 #王陵大墓# 话题！ °详解世遗 “丝绸之路:长安-天山廊道的路网”",
u"#一带一路# #这匹马让你看尽大唐繁华# 我们唐三彩系列的第四篇，讲“发展”！中西方文化的交融，促成了三彩艺术的大发展  #约会博物馆# 快看看我们的《从三彩牵马俑看盛唐气象之发展篇》 °从三彩牵马俑看盛唐气象之发展篇",
u"【这是一条神奇的“路”】#一带一路# 国际合作高峰论坛本周日就要在北京举行啦！三年来，对中国互粉的小伙伴越来越多，“一带一路”的朋友圈，也已有100多个~但你知道哪里最浪漫？哪里最神奇？哪里最迷人？哪里最震撼吗？满世界逛吃逛吃的中国游客们，这份属于#一带一路#的旅游攻略你必须g ​​​​...展开全文",
u"#一带一路#乌兹别克斯坦总统夫妇访华。人民大会堂，欢迎仪式。",
u"#一带一路# 【有朋自远方来，别连名字都念错】白俄罗斯的英文是什么？ 可不是White Russia哦！本周日“一带一路”国际合作高峰论坛就要开幕了那么多国家的名字你都会念吗？ 善良的小编加班为大家准备了补习视频，两分钟帮你变学霸，快来戳视频学习吧！  L英语环球广播的秒拍视频",
u"#一带一路# 进站硬是检查了三次 2淄博·淄博火车站",
u"【我们的#一带一路#】3年多来，习近平主席提出的“一带一路”宏伟构想，从理念构想到人心聚合，从顶层设计到项目落实，各领域合作不断开花结果，得到沿线各国的热情回应，开辟了共同发展的广阔空间。L人民日报的秒拍视频",
)

# stopWords = stopwords.words('english')
# print stopWords

stopWords = {",", "?", "、", "。", "“", "”", "《", "》", "！", "，", "：", "；", "？",
"的","了","在","是","我","有","和","就","不","人","都","一","一个","上","也","很","到","说","要","去","你","会","着","没有","看","好","自己","这"}

vectorizer = TfidfVectorizer(ngram_range=(1,1), stop_words = stopWords)
vectorizer.fit(documents)
words =  vectorizer.get_feature_names()
test_set = []
for word in words:
  test_set.append(str(word))
# print test_set
for line in test_set:
	print line.encode('utf-8')
print vectorizer.transform(test_set).toarray().sum(1)
