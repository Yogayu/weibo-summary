#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

import subprocess

# RawData -> weboData 数据预处理
# process_keyword_data = subprocess.Popen(["python","util/KeywordXML2TXT.py"]); process_keyword_data.wait()
# process_topic_data = subprocess.Popen(["python","util/TopicXML2TXT.py"]); process_topic_data.wait()

#多种算法摘要生成

# random 		 = subprocess.Popen(["python","Random.py"]); random.wait()

# MostRecent 	 = subprocess.Popen(["python","MostRecent.py"]); MostRecent.wait()

# TFIDF 		 = subprocess.Popen(["python","TFIDF.py"]); TFIDF.wait()

# HybirdTFIDF  = subprocess.Popen(["python","Hybird-TFIDF.py"]); HybirdTFIDF.wait()

# TextRank 	 = subprocess.Popen(["python","TextRank.py"]); TextRank.wait()

# 计算ROUGE值
# cd_ROUGE 	 	 = subprocess.Popen(["cd ROUGE"]); Cd_ROUGE.wait()
# caculate_ROUGE	 = subprocess.Popen(["java","-jar","rouge2.0_0.2.jar"]); caculate_ROUGE.wait()
