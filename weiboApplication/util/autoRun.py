#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
import subprocess
import sys, os
sys.path.append('../')
from config import *

# 设置编码格式
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2 or args[0] == 'None' or args[1] == 'None':
        print('error args - autoRun')
        exit()
    topic_name = args[0]
    topic_type = args[1]
    file_path = get_base_dir()


    RawData -> weboData 数据预处理并存入数据库
    print("数据预处理并存入数据库")
    if topic_type == 'Keyword':
        file_path += '/util/KeywordXML2TXT.py'
        process_keyword_data = subprocess.Popen(["python",file_path,topic_name]); process_keyword_data.wait()
    elif topic_type == 'Topic':
        file_path += '/util/TopicXML2TXT.py'
        process_topic_data = subprocess.Popen(["python",file_path,topic_name]); process_topic_data.wait()

获取关键字并存入数据库
file_path = get_base_dir() + '/util/keywords.py'
keywords   = subprocess.Popen(["python","keywords.py",topic_name]); keywords.wait()


# 生成算法摘要并存入数据库

random = subprocess.Popen(["python", get_base_dir() + "/Algorithms/Random.py", topic_name]); random.wait()

MostRecent 	 = subprocess.Popen(["python", get_base_dir() + "/Algorithms/MostRecent.py", topic_name]); MostRecent.wait()

TFIDF 		 = subprocess.Popen(["python", get_base_dir() + "/Algorithms/TFIDF.py", topic_name]); TFIDF.wait()

HybirdTFIDF  = subprocess.Popen(["python", get_base_dir() + "/Algorithms/Hybird-TFIDF.py", topic_name]); HybirdTFIDF.wait()

TextRank 	 = subprocess.Popen(["python", get_base_dir() + "/Algorithms/TextRank.py", topic_name]); TextRank.wait()

# 计算ROUGE值并将结果存入数据库
calculateAllROUGE = subprocess.Popen(["python", get_base_dir() + "/util/calculateAllRouge.py"]); randomResult.wait()

# subprocess.Popen(["python","getRandomResult.py"]); randomResult.wait()

# 多次Random 评估值
# randomResult = subprocess.Popen(["python","getRandomResult.py"]); randomResult.wait()


