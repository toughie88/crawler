#!/usr/bin/python
#coding:utf-8
#ｕｒｌ调度管理器
import html_downloader
import html_outputer
import html_parser
import url_manager


class SpiderMain():
    def __init__(self):
        self.urls = url_manager.UrlManager()#url 管理器
        self.downloader = html_downloader.HtmlDownloader()#下载器
        self.parser = html_parser.HtmlParser()#解析器
        self.outputer = html_outputer.HtmlOutputer()#输出器

    #爬虫调度器
    def craw(self,root_url):
        #将入口ｕｒｌ添加到ｕｒｌ管理器中
        self.urls.add_new_url(root_url)
        #循环ｕｒｌ管理器中的ｕｒｌ，获取还没下载的新的ｕｒl
        count = 1
        while self.urls.has_new_url():
            try:#有些ｕｒｌ不能访问，可能出现错误，所以ｔｒｙ一下
                #记录这是当前的爬取的是哪个以及第几个ｕｒｌ
                new_url = self.urls.get_new_url()
                print 'craw %d : %s'%(count,new_url)
                #将新的ｕｒｌ的ｈｔｍｌ下载
                html_cont = self.downloader.download(new_url)
                #将新的ｕｒｌ和ｈｔｍｌ传入解析器进行解析，获得新的ｕｒｌｓ和ｄａｔａ
                new_urls,new_data = self.parser.parse(new_url,html_cont)
                #将新得到ｕｒｌｓ添加到ｕｒｌ管理器
                self.urls.add_new_urls(new_urls)
                #将新的数据进行收集
                self.outputer.collect_data(new_data)

                if count == 1000:
                    break
                count+=1
            except:
                print 'craw failed'
        # 最后输出收集好的数据
        self.outputer.output_html()



#主函数入口
if __name__=="__main__":
    root_url = "http://baike.baidu.com/item/%E7%8E%8B%E5%AE%9D%E5%BC%BA/40464"
    #创建爬虫
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)