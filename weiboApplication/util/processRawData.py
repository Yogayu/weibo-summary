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


    # RawData -> weboData 数据预处理并存入数据库
    print("数据预处理并存入数据库")
    if topic_type == 'Keyword':
        file_path += '/util/KeywordXML2TXT.py'
        process_keyword_data = subprocess.Popen(["python",file_path,topic_name]); process_keyword_data.wait()
    elif topic_type == 'Topic':
        file_path += '/util/TopicXML2TXT.py'
        process_topic_data = subprocess.Popen(["python",file_path,topic_name]); process_topic_data.wait()
