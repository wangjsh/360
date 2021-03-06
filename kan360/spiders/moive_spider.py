# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from kan360.pipelines import Kan360Pipeline
from kan360.notifyJava import notifyJava
from kan360.managedata import formatProName
import time

class MoiveSpider(CrawlSpider):
    name = "360"
    allowed_domains = ['www.360kan.com']
    year = time.strftime('%Y',time.localtime(time.time()))
    #运行的时候      紧紧考虑这一年的
    start_urls = ['http://www.360kan.com/dianshi/list.php?cat=all&year='+ year +'&area=all&act=all']
    
    #start_urls = ['http://www.360kan.com/dianshi/list.php?cat=all&year=all&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2016&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2015&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2014&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2013&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2012&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2011&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2010&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2009&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2008&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2007&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=2006&area=all&act=all', 'http://www.360kan.com/dianshi/list.php?cat=all&year=other&area=all&act=all']
    #负责操作数据库的一个对象
    pipe = Kan360Pipeline()
    totalNum = 0
    insertNum = 0

    #在start_url中提取电视节目页面的url
    def parse(self,response):
        sel = Selector(response)
        tvinfos = sel.xpath('//ul[@class="result-list clearfix"]/li')
        count = 0#记录新插入的节目总数
        for e in tvinfos:
            nameli = e.xpath('./div[@class="cont"]/p[@class="video-title"]/a/text()').extract()
            actorli = e.xpath('./div[@class="cont"]/p[@class="video-information"][1]/a/text()').extract()
            if len(nameli) == 0 or len(actorli) == 0:
                continue
            #处理演员信息
            i = 0
            proActor = ''
            while i < len(actorli) - 1:
                proActor = proActor + actorli[i].strip() + ','
                i = i + 1
            proActor = proActor + actorli[len(actorli) - 1]
            proName = formatProName(nameli[0].strip()).strip()
            if len(proName) == 0:
                proName = '_null_'
            num = self.pipe.search(proName)
            #数据库中没有记录则插入此新纪录
            if num < 1:
                item = {'name': proName, 'zhuyan': proActor}
                #self.pipe.process_item(item)
                count = count + 1
            else:
                pass
        self.totalNum = self.totalNum + len(tvinfos)
        self.insertNum = self.insertNum + count
        nextUrl = sel.xpath('//a[@class="page-next"]/@href').extract()
        if len(nextUrl) > 0:
            yield Request(nextUrl[0], callback = self.parse)
        else:
            pass

    #closed 方法  判断爬虫结束方式，若完成爬取正常结束，则通知相关建立索引进程数据已经更新，重新建立索引
    def closed(self, reason):
        if reason == "finished":
            print 'scrapy completed crawling, closed. Notify java process to create index_file.'
            print 'the new added program numbers is: ', self.insertNum
            print 'the number of programs extracted in this page is: ', self.totalNum
            notifyJava()
        else:
            print 'scrapy was closed in other ways.'
