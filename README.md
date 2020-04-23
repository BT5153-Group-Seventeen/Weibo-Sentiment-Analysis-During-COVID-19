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
#### Basic SnowNLP
Code: ```Model1_Basic_SnowNLP.ipynb```  

Data: ```df_final.csv```  

This model is built directly on original SnowNLP (you just need to download package and import it without any adjustment).  

#### Re-trained SnowNLP
Code: ```Model2_Re-trained_SnowNLP.ipynb```  

Data: ```5,000,000 Weibo Comments```,```df_final.csv```  

Corpus and Retrained Marshal: ```sentiment.marshal.3```  

This model is trained on 5,000,000 Weibo comments. The training process will take about 25 hours in total. You can skip the training process by directly call sentiment.marshal retrained. You also need to change ```snownlp\sentiment\__init__.py``` as follows:  

```
import os
import codecs
import jieba

from .. import normal
# from .. import seg
from ..classification.bayes import Bayes

# data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                        'sentiment.marshal')

data_path = 'D:\MSBA\Semester_2\BT5153\Group Project\sentiment.marshal' 
# download the retrained sentiment.marshal and change call path here

class Sentiment(object):

    def __init__(self):
        self.classifier = Bayes()

    def save(self, fname, iszip=True):
        self.classifier.save(fname, iszip)

    def load(self, fname=data_path, iszip=True):
        self.classifier.load(fname, iszip)

    def handle(self, doc):
        words = jieba.lcut(doc) ## pleace word splitting method by Jieba
        words = normal.filter_stop(words)
        return words
```  
See reference: https://zhuanlan.zhihu.com/p/30061051, https://blog.csdn.net/weixin_42007766/article/details/89824318  

#### Dictionary Matching Method
Code: ```Model3_jieba_sentiment.ipynb```   

Data: ```df_final.csv```  
(Since the dictionaries are confidential, you can go to the following website link to request perssion from this author)  

See reference: https://blog.csdn.net/qq_41185868/article/details/84864905#comments

#### Machine Learning Models based on Labeled 3000 reposts
Code: ```Model4_based on labeled data .ipynb```   

Data: ```random_3000_with_label.csv```  

(Please note that results of this model are used for visualization)  

## Sentiment Visualization
Code: ```Model_result_visualization.ipynb```   

Data: ```user_all.csv```  
