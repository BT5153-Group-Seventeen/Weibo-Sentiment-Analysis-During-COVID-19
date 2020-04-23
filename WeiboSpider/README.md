# WeiboSpider
This is a sina weibo spider built by scrapy

**这是一个持续维护的微博爬虫开源项目,有任何问题请开issue**

更多关于微博爬虫的介绍请移步:[微博爬虫总结：构建单机千万级别的微博爬虫系统](http://www.nghuyong.top/2018/09/12/spider/%E5%BE%AE%E5%8D%9A%E7%88%AC%E8%99%AB%E6%80%BB%E7%BB%93%EF%BC%9A%E6%9E%84%E5%BB%BA%E5%8D%95%E6%9C%BA%E5%8D%83%E4%B8%87%E7%BA%A7%E5%88%AB%E7%9A%84%E5%BE%AE%E5%8D%9A%E7%88%AC%E8%99%AB%E7%B3%BB%E7%BB%9F/)

## 项目说明
该项目分为3个分支，以满足不同的需要

|    分支   | 特点 | 单机每日抓取量 |
| :---: | :----: |:----: |
| [simple](https://github.com/nghuyong/WeiboSpider/tree/simple) | 单账号 | 十万级|
| [master](https://github.com/nghuyong/WeiboSpider/tree/master) | 账号池 | 百万级|
| [senior](https://github.com/nghuyong/WeiboSpider/tree/senior) | 账号池+分布式 | 千万级+ | 


该项目爬取的数据字段说明，请移步:[数据字段说明与示例](./data_stracture.md)

已经在senior分支的基础上新增了[search分支](https://github.com/nghuyong/WeiboSpider/tree/search)，用于微博关键词搜索

## Change log
- 2019/05/07 添加IP池的示例代码
- 2019/05/07 全面修复历史问题，增加用户的标签，评论的点赞，微博的发布平台/表情/图片/视频等新的字段
- 2018/10/13 添加[微博搜索分支](https://github.com/nghuyong/WeiboSpider/tree/search)
- 2018/9/30 添加布隆过滤器

## 如何使用
下面是search分支，在senior分支基础上添加了关键词搜索功能

### 克隆本项目 && 安装依赖
本项目Python版本为Python3.6
```bash
git clone git@github.com:nghuyong/WeiboSpider.git
cd WeiboSpider
pip install -r requirements.txt
```
除此之外，还需要安装mongodb，phantomjs和redis，这个自行Google把

### 购买账号
小号购买地址: http://www.wbxiaohao.com/ 更多小号购买的网站参考[这里](https://github.com/CUHKSZ-TQL/WeiboSpider_SentimentAnalysis/issues/2#issuecomment-505842345).

需要购买**绑号无验证码类型的微博小号**（重点！）

![](./images/xiaohao_shop.png)

购买越多，sina/settings.py 中的延迟就可以越低，并发也就可以越大

**将购买的账号复制到`sina/account_build/account.txt`中，格式与`account_sample.txt`保持一致**。

### 构建账号池

```bash
python sina/account_build/login.py
```
运行截图:

![](./images/account_build_screenshot.png)

这是你的mongodb中将多一个账号表，如下所示:

![](./images/account.png)

### 加入代理IP

请重写[fetch_proxy](https://github.com/nghuyong/WeiboSpider/blob/search/sina/middlewares.py#L53)方法，该方法需要返回一个代理ip

### 初始化redis
分布式爬虫是所有的爬虫都从redis中获取URL

所以首先向redis中填充初始的URL

请将`sina/redis_init.py`中的 关键词 和 日期修改成你自己需要的

```bash
python sina/redis_init.py
```

### 运行爬虫
```bash
scrapy crawl weibo_spider 
```
可以打开新的终端，开多个进程。

运行截图:

![](./images/redis.png)

导入pycharm后，也可以直接执行`sina/spider/weibo_spider.py`

该爬虫是示例爬虫，将爬取的是2017-07-30 到 2018-07-30 关键词为转基因的微博数据和用户数据。

可以根据你的实际需求改写示例爬虫。

## 速度说明

一个页面可以抓取10则微博数据

下表是我的配置情况和速度测试结果

|    爬虫配置   | 配置值 |
| :---: | :----: |
| 账号池大小  | 200+ |
| 单个爬虫 CONCURRENT_REQUESTS | 16 |
| 单个爬虫 DOWNLOAD_DELAY | 0.1s|
| 单个爬虫每分钟抓取网页量 | 250+ |
| 单个爬虫每分钟抓取数据量 | 2500+ |
| 爬虫进程数  | 8 |
| 总体每分钟抓取网页量 | 2000+ | 
| 总体每分钟抓取数据量 | 20000+ |
| 总体一天抓取数据量 | **2880万+** |

实际速度和你自己电脑的网速/CPU/内存有很大关系。