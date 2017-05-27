#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

import csv
import codecs
import sys

sys.path.append('../')
from weiboApplication.weiboModel import *

headers = ['ROUGE-Type', 'Task Name', 'System Name', 'Avg_Recall',
           'Avg_Precision', 'Avg_F-Score', 'SUM', 'Num Reference Summaries']

rows = []
resultItems = []
with open('results.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        rouge_sum = float(row['Avg_Precision']) + \
            float(row['Avg_Precision']) + float(row['Avg_F-Score'])
        topic_name = row['Task Name']
        method_name = row['System Name']
        recall = row['Avg_Recall']
        FScore = row['Avg_F-Score']
        precision = row['Avg_Precision']
        refNum = row['Num Reference Summaries']

        rows.append(('ROUGE-1', topic_name, method_name,
                     recall, precision, FScore,
                     rouge_sum, refNum))

        resultItems.append(Result(method_name, topic_name, precision, recall, FScore, rouge_sum))

# 将结果写入文件中
# with open('RandomResults.csv','a+') as f:
#     f.write(codecs.BOM_UTF8)
#     writer = csv.writer(f)
#     writer.writerows(rows)

# 中文编码有问题，Excel打开之后会乱码
with open('AllResults.csv','a+') as f:
    f.write(codecs.BOM_UTF8)
    writer = csv.writer(f)
    writer.writerows(rows)

# save to the database
for resultItem in resultItems:
    resultItem.add()
