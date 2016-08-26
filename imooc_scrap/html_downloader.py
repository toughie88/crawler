#coding:utf-8
#下载器
import urllib2


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None

        response = urllib2.urlopen(url)
        #如果读取失败
        if response.getcode() !=200:
            return  None
        #读取成功，返回内容
        return response.read()