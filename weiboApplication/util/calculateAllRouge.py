#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
# 存储摘要性能值

from subprocess import call
import sys
sys.path.append('../')
from config import *

file_path = get_base_dir() + '/Data/ROUGE/'
system_summary_path = file_path + 'test-summarization/system'

call(['rm', '.DS_Store'],cwd=system_summary_path)

call('java -jar rouge2.0_0.2.jar', shell=True, cwd=file_path)

call(['python processResult.py'], shell=True, cwd=get_base_dir() + '/util/')
