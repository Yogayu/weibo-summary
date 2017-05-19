 #! /usr/bin/env python
 # coding=utf-8
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# from nltk.corpus import stopwords
from textrank4zh import Segmentation
import codecs
import numpy as np
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

# stopWords = stopwords.words('english')
stopWords = [",", "?", "、", "。", "“", "”", "《", "》", "！", "，", "：", "；", "？",
"的","了","在","是","我","有","和","就","不","人","都","一","一个","上","也","很","到","说","要","去","你","会","着","没有","看","好","自己","这"]

vectorizer = CountVectorizer(stop_words = stopWords)
transformer = TfidfTransformer()

topic_name = ""
train_set = []
# with open('data/'+topic.rstrip()+'.txt') as data:
print "reading topics from 05/16"
with open('topic_list-5-16.txt') as f:
    content = f.readlines()
    seg = Segmentation.Segmentation()
    for topic in content:
        print "\n话题:"
        topic_name = topic.rstrip()
        print topic.rstrip()
        train_set = []
        line_tweet = []
        split_line_tweet = []
        count = 0
        with open('weiboData/'+topic.rstrip()+'.txt') as data:
            for tweet in data.readlines():
                #原始每行数据
                line_tweet.append(tweet)
                #中文分词之后的数据
                result = seg.segment(text=tweet, lower=True)
                count = count + 1
                for ss in result.words_no_filter:
                    split_line_tweet.append(' '.join(ss))
                if split_line_tweet != []:
                    train_set.append(split_line_tweet[0])
                split_line_tweet = []
        tfidf = transformer.fit_transform(vectorizer.fit_transform(train_set))
        word = vectorizer.get_feature_names() #所有文本的关键字
        weight = tfidf.toarray()              #对应的tfidf矩阵
        sums = weight.sum(1)
        sorted_indices = np.argsort(sums)

        # 将结果存入文件
        sFilePath = '/Users/apple/scrapingEnv/weibo-summary/resultData/tf-idf'
        output_file = ""
        if not os.path.exists(sFilePath) :
            os.mkdir(sFilePath)
        out = open(sFilePath + '/'+ topic_name +'-'+'tf-idf'+'.txt','w+')

        # print sorted_indices
        print "best"
        print sums[sorted_indices[-1]]
        print sums[sorted_indices[-2]]
        print sums[sorted_indices[-3]]
        print sorted_indices[-1]
        print line_tweet[sorted_indices[-1]]
        print "second best"
        print sums[sorted_indices[-2]]
        print line_tweet[sorted_indices[-2]]

        output_file = output_file + line_tweet[sorted_indices[-1]]
        output_file = output_file + line_tweet[sorted_indices[-2]]
        output_file = output_file + line_tweet[sorted_indices[-3]]
        
        out.write(output_file)
        out.close()

        # recalculate 1
        seenWords = stopWords + train_set[sorted_indices[-1]].split(' ')
        vectorizer2 = CountVectorizer(stop_words = seenWords)
        trainVectorizerArray = vectorizer2.fit_transform(train_set).toarray()
        transformer2 = TfidfTransformer()
        transformer2.fit(trainVectorizerArray)
        sums = transformer2.transform(trainVectorizerArray).toarray().sum(1)
        sorted_indices = np.argsort(sums)
        print "recalculate 1"
        print sums[sorted_indices[-1]]
        print sorted_indices[-1]
        print line_tweet[sorted_indices[-1]]

        # recalculate 2
        seenWords2 = seenWords + train_set[sorted_indices[-1]].split(' ')
        vectorizer3 = CountVectorizer(stop_words = seenWords2)
        trainVectorizerArray = vectorizer3.fit_transform(train_set).toarray()
        transformer3 = TfidfTransformer()
        transformer3.fit(trainVectorizerArray)
        sums = transformer3.transform(trainVectorizerArray).toarray().sum(1)
        sorted_indices = np.argsort(sums)
        print "recalculate 2"
        print sums[sorted_indices[-1]]
        print sorted_indices[-1]
        print line_tweet[sorted_indices[-1]]