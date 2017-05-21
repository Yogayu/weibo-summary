#-*- encoding:utf-8 -*-
"""
@author:youxinyu
"""

from textrank4zh import Segmentation
import codecs

# 获取分词之后的数据集


def get_train_set(topic):
    # 分词之后的数据集
    train_set = []
    # 原始未分词数据集
    line_tweet = []
    split_line_tweet = []
    seg = Segmentation.Segmentation()
    with open('weiboData/'+topic.rstrip()+'.txt') as data:
        for tweet in data.readlines():
            # 原始每行数据
            line_tweet.append(tweet)
            # 中文分词之后的数据
            result = seg.segment(text=tweet, lower=True)
            for ss in result.words_no_filter:
                split_line_tweet.append(' '.join(ss))
            if split_line_tweet != []:
                train_set.append(split_line_tweet[0])
            split_line_tweet = []
    return (train_set, line_tweet)

# 获取停等词


def get_stop_words():
    stop_words = []
    stop_words_file = Segmentation.get_default_stop_words_file()
    # if type(stop_words_file) is str:
    for word in codecs.open(stop_words_file, 'r', 'utf-8', 'ignore'):
        stop_words.append(word.strip())
    return stop_words
