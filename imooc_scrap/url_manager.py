#coding:utf-8
#ｕｒｌ管理器
class UrlManager(object):
    def __init__(self):
        #待爬取的ｕｒｌ列表
        self.new_urls = set()
        #已经爬取过的ｕｒｌ
        self.old_urls = set()
    #添加新的ｕｒｌ，添加一条
    def add_new_url(self, url):
        #首先判断是否是空的
        if url is None:
            return
        #判断是不是已经爬过或者在待爬列表中
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    #添加一组ｕｒｌ
    def add_new_urls(self, urls):
        #ｕｒｌｓ为空，或者列表长度为０
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
        #从新的ｕｒｌ中移除并且添加到老的ｕｒｌ中
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url