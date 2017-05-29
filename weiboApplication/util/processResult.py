#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

import csv
import codecs
import sys

sys.path.append('../')
from config import *
from app import Result

if __name__ == "__main__":

    headers = ['ROUGE-Type', 'Task Name', 'System Name', 'Avg_Recall',
               'Avg_Precision', 'Avg_F-Score', 'SUM', 'Num Reference Summaries']

    rows = []
    resultItems = []
    path = get_base_dir() + '/Data/ROUGE/' + 'results.csv'
    with open(path) as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            try:
                precision = float(row['Avg_Precision'].replace("�", "0.00"))
            except:
                precision = 0.000 
            
            try:
                recall = float(row['Avg_Recall'].replace("�", "0.00"))
            except:
                recall = 0.000

            try:
                FScore = float(row['Avg_F-Score'].replace("�", "0.00"))
            except:
                FScore = 0

            rouge_sum = precision + recall + FScore

            topic_name = row['Task Name']
            method_name = row['System Name'].replace("SYSSUM.TXT", "")
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
    file_path = get_base_dir() + '/Data/ROUGE/' + 'AllResults.csv'
    # 中文编码有问题，Excel打开之后会乱码
    with open(file_path,'a+') as f:
        f.write(codecs.BOM_UTF8)
        writer = csv.writer(f)
        writer.writerows(rows)

    # save to the database
    for resultItem in resultItems:
        resultItem.add()

    print ('process results success!')