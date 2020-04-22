# Weibo-Sentiment-Analysis-During-COVID-19
In order to analyze the sentiment orientation on Chinese social platform, our group scraped raw reposts during the period when domestic COVID is most series(1.20-3.09) from Weibo and built different models to predict the sentiment scores of these reposts.

## Data Crawling
We applied a ready-made package "WeiboSpider" to crawl data. For package, please refer to the Folder "WeiboSpider".

1. Install Dependencies
mongodb (you need to create database `Sina`)
phantomjs
redis
requirements.txt

2. Construct Account Pool:
You can buy some Weibo accounts, paste them in txt file `WeiboSpider/sina/account_build/account.txt`.

3. Customize the retrieval criteria
You change the dates, keyword, and filter (sort='hot'/'time') in `WeiboSpider/sina/redis_init.py` to crawl data you needed.
```
url_format = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime={}&endtime={}&sort=hot&page=1"
# keyword for searching
keyword = "新冠肺炎"
# startdate for crawling
date_start = datetime.datetime.strptime("2020-01-20", '%Y-%m-%d')
# enddate for crawling
date_end = datetime.datetime.strptime("2020-03-09", '%Y-%m-%d')
time_spread = datetime.timedelta(days=1)
```
4. Start Crawling
Mac User:
Windows User: For windows user, since there are some commands in crawling codes written by linux language, you are strongly suggested to use Ubuntu or virtual machines for crawling. 
```
$ redis-server
$ cd /mnt/c/users/asus/documents/github/WeiboSpider (please change to your own path)
$ python sina/account_build/login.py (login all your weibo accounts in accounts pool)
$ python sina/redis_init.py (crawling criteria update)
$ cd /mnt/c/users/asus/documents/github/WeiboSpider/sina/spiders (please change to your own path)
$ scrapy runspider weibo_spider.py
```
You can open several severs to crawl in parallel.

5. Final Database in MongoDB
Repost info and user info will be scraped.

See reference: https://github.com/CUHKSZ-TQL/WeiboSpider_SentimentAnalysis

## Sentiment Prediction
Since the data we crawled is unlabeled, traditional supervised learning cannot be applied. Here we applied four methods to solve this problem: ```SnowNLP```, ```Re-trained SnowNLP on 5,000,000 Weibo Corpus```, ```Dictionary Matching```, and ```Supervised Learning based on small proportion of total data```.
### Basic SnowNLP
Code: ```Model1_Basic_Snownlp.ipynb```
Data: ```df_final.csv```
This model is built directly on original SnowNLP (you just need to download package and import it without any adjustment). 
### Re-trained SnowNLP
Code:
Data:
