#-*- encoding:utf-8 -*-
from utilities import *
import os
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass


topic_name = "#校园网大规模病毒攻击#"
segment_set = get_segment_set("ROUGE/reference/" + topic_name + ".txt")
json_print(segment_set)

sFilePath = 'lib/rouge2.0-0.2-distribute/test-summarization/reference/'
output_file = ""
if not os.path.exists(sFilePath):
    os.mkdir(sFilePath)
out = open(sFilePath + topic_name + '-Hybrid-TFIDF_Reference2.txt', 'w+')

for line in segment_set:
	output_file += line + '\n'

out.write(output_file)
out.close()
