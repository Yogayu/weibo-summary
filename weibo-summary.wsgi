#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/weibo-summary/")

sys.path.append('/var/www/weibo-summary/weiboApplication')

from weiboApplication.app import app as application
