#!/usr/bin/env python
# encoding: utf-8
import redis
import sys
import os
import datetime
sys.path.append(os.getcwd())
from sina.settings import LOCAL_REDIS_HOST, LOCAL_REDIS_PORT

r = redis.Redis(host=LOCAL_REDIS_HOST, port=LOCAL_REDIS_PORT)
for key in r.scan_iter("weibo_spider*"):
    r.delete(key)
    print('删除成功')

url_format = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime={}&endtime={}&sort=hot&page=1"
# keyword for searching
keyword = "新冠肺炎"
# startdate for crawling
date_start = datetime.datetime.strptime("2020-01-20", '%Y-%m-%d')
# enddate for crawling
date_end = datetime.datetime.strptime("2020-03-09", '%Y-%m-%d')
time_spread = datetime.timedelta(days=1)
while date_start < date_end:
    next_time = date_start + time_spread
    url = url_format.format(keyword, date_start.strftime("%Y%m%d"), next_time.strftime("%Y%m%d"))
    r.lpush('weibo_spider:start_urls', url)
    date_start = next_time
    print('添加{}成功'.format(url))
