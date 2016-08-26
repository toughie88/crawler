# 爬取百度百科1000条数据

------

练手项目，一个简单的python爬虫，从百度百科页面：入口页面为[王宝强][1]，爬取关于王宝强的1000条数据。


----------
## 爬取内容与格式 ##

 - 词条页面url
 - 词条名称
 - 词条概述
 
输出文件为html文本
格式以列表的形式进行输出如下所示：

<table>
<tr>
<td>url</td>
<td>词条名称</td>
<td>简介</td>
</tr>
<tr>
<td>http://baike.baidu.com/item/%E7%8E%8B%E5%AE%9D%E5%BC%BA/40464</td>
<td>王宝强</td>
<td>王宝强，1984年5月29日出生于河北省邢台市，中国内地男演员、导演。王宝强6岁开始练习武术，8岁在嵩山少林寺做俗家弟子。2003年，凭借剧情片《盲井》获得第40届台湾电影金马奖最佳新演员奖[1-2]  。2004年，因参演冯小刚执导的剧情片《天下无贼》而获得关注。2008年，凭借《士兵突击》中许三多一角获得第24届中国电视金鹰奖最具人气男演员奖以及观众喜爱的电视剧男演员奖[3-4]  ；同年，因出演《我的兄弟叫顺溜》中顺溜一角而受到广泛关注[5]  。2010年，出演战争剧《为了新中国前进》[6]  。2011年，凭借喜剧片《Hello!树先生》获得俄罗斯、美国纽约、意大利电影节最佳男主角奖及亚太电影奖。2012年，与徐峥继《人在囧途》再度合作的《人再囧途之泰囧》刷新华语电影票房纪录。2014年，相继主演了科幻片《冰封：重生之门》、动作片《一个人的武林》[7]  。2015年，主演了陈凯歌执导的奇幻片《道士下山》；12月，主演喜剧片《唐人街探案》[8-9]  。2016年，执导了个人电影处女作《大闹天竺》[10]  。2016年8月14日凌晨，王宝强在微博发离婚声明，与妻子解除婚姻关系。[11-12]  15日上午9时许，王宝强本人在律师陪同下来到北京朝阳法院，起诉其妻马蓉要求离婚。朝阳法院经审查符合立案条件，已正式受理此案。[13]  </td>
</tr>
</table>
以上述形式爬取了1000条相关的消息：


----------
## 项目结构：##

> * 爬虫调度端
参见文件：spider_main.py
在其中实例化了：
url管理器
下载器
解析器
输出器
传入入口url.
代码：
```python
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

```
> * url 管理器，管理还未爬取和已经爬取url
```python
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

```
> * url下载器：url管理器将待爬取的url传送给网页下载器，进行下载，然后以字符串的形式传递给网页解析器进行解析。
```python
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
```
> * 解析器，将需要的内容进行解析：
解析的过程需要分析，利用浏览器的查看元素功能查看对应内容的格式进行解析：
这里使用了BeautifulSoup 框架,解析器使用的是：html.parser
```python
#coding:utf-8
import re
import urlparse
from bs4 import BeautifulSoup


class HtmlParser(object):
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        #创建ｂｅａｕｔｉｆｕｌＳｏｕｐ对象
        soup = BeautifulSoup(html_cont,#待解析的内容
                             'html.parser',#ｈｔｍｌ解析器
                             from_encoding='utf-8')#编码
        #本地方法,获取新的ｕｒｌｓ
        new_urls = self._get_new_urls(page_url,soup)
        #本地方法，获取有用的数据
        new_data = self._get_new_data(page_url,soup)

        return new_urls,new_data


    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        #在分析过程中，百科的内链接是‘/view/123.htm’的形式，所以需要匹配相关的内容
        links = soup.find_all('a',href=re.compile(r"/view/\d+\.htm"))
        for link in links:
            new_url=link['href']
            #如前所述，匹配的形式是“view/123.htm”的形式，必须得加上page_url 即，当前页面的ｕｒｌ。
            new_full_url = urlparse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls

    #解析数据
    def _get_new_data(self, page_url, soup):
        res_data = {}
        # 打开页面，查看元素
        # <dd class="lemmaWgt-lemmaTitle-title">
        # <h1 >Python</h1>
        #标题标签都是这个格式
        title_node = soup.find('dd',class_="lemmaWgt-lemmaTitle-title").find('h1')

        res_data['title'] = title_node.get_text()


        #内容属性部分
        # < div
        #
        # class ="lemma-summary" label-module="lemmaSummary" >
        #
        # < div
        #
        # class ="para" label-module="para" > Python（英国发音： / ˈpaɪθən / 美国发音： / ˈpaɪθɑːn / ）, 是一种 < a target="_blank" href="/view/125370.htm" > 面向对象 < / a > 、解释型 < a target="_blank" href="/view/2561555.htm" > 计算机程序设计语言 < / a > ，由 < a target="_blank" href="/view/2975166.htm" > Guido van Rossum < / a > 于1989年发明，第一个公开发行版发行于1991年。 < / div > < div class ="para" label-module="para" > Python是纯粹的 < a target="_blank" href="/view/20965.htm" > 自由软件 < / a > ， < a target="_blank" href="/subview/60376/5122159.htm" data-lemmaid="3969" > 源代码 < / a > 和 < a target="_blank" href="/view/592974.htm" > 解释器 < / a > CPython遵循 < a target="_blank" href="/view/130692.htm" > GPL < / a > ( < a target="_blank" href="/view/36272.htm" > GNU < / a > General Public License)协议 < sup >[1] < / sup > < a class ="sup-anchor" name="ref_[1]_21087" > & nbsp; < / a >
        #
        # 。 < / div > < div
        #
        # class ="para" label-module="para" > Python语法简洁清晰，特色之一是强制用空白符(white space)作为语句缩进。 < / div > < div class ="para" label-module="para" > Pref="/view/125370.htm" > 面向对象 < / a > 、解释型 < a target="_blank" href="/view/2561555.htm" > 计算机程序设计语言 < / a > ，由 < a target="_blank" href="/view/2975166.htm" > Guido van Rossum < / a > 于1989年发明，第一个公开发行版发行于1991年。 < / div >
        summary_node = soup.find('div',class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()

        # url
        res_data['url'] = page_url

```
> * 输出器，将解析好的内容以指定的形式输入到指定的文件：
```python
#coding:utf-8
#ｈｔｍｌ输出器
class HtmlOutputer(object):

    def __init__(self):
        self.datas =[]

    #收集数据
    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        #写入文件，以ｈｔｍｌ的形式输出
        fout = open('output.html','w')

        fout.write("<html>")
        fout.write("<body>")
        #以表格的形式输出
        fout.write("<table>")
        #ptrhon默认编码是ａｓｃｉｉ　所以需要显式的定义编码
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
            fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
```

## 输出文件预览 ##
<table><tr><td>http://baike.baidu.com/item/%E7%8E%8B%E5%AE%9D%E5%BC%BA/40464</td><td>王宝强</td><td>
王宝强，1984年5月29日出生于河北省邢台市，中国内地男演员、导演。王宝强6岁开始练习武术，8岁在嵩山少林寺做俗家弟子。2003年，凭借剧情片《盲井》获得第40届台湾电影金马奖最佳新演员奖[1-2] 
。2004年，因参演冯小刚执导的剧情片《天下无贼》而获得关注。2008年，凭借《士兵突击》中许三多一角获得第24届中国电视金鹰奖最具人气男演员奖以及观众喜爱的电视剧男演员奖[3-4] 
；同年，因出演《我的兄弟叫顺溜》中顺溜一角而受到广泛关注[5] 
。2010年，出演战争剧《为了新中国前进》[6] 
。2011年，凭借喜剧片《Hello!树先生》获得俄罗斯、美国纽约、意大利电影节最佳男主角奖及亚太电影奖。2012年，与徐峥继《人在囧途》再度合作的《人再囧途之泰囧》刷新华语电影票房纪录。2014年，相继主演了科幻片《冰封：重生之门》、动作片《一个人的武林》[7] 
。2015年，主演了陈凯歌执导的奇幻片《道士下山》；12月，主演喜剧片《唐人街探案》[8-9] 
。2016年，执导了个人电影处女作《大闹天竺》[10] 
。2016年8月14日凌晨，王宝强在微博发离婚声明，与妻子解除婚姻关系。[11-12] 
  15日上午9时许，王宝强本人在律师陪同下来到北京朝阳法院，起诉其妻马蓉要求离婚。朝阳法院经审查符合立案条件，已正式受理此案。[13] 

</td></tr><tr><td>http://baike.baidu.com/view/10812277.htm</td><td>百度百科：多义词</td><td>
百度百科里，当同一个词条名可指代含义概念不同的事物时，这个词条称为多义词。如词条“苹果”，既可以代表一种水果，也可以指代苹果公司，因此“苹果”是一个多义词。
</td></tr><tr><td>http://baike.baidu.com/view/793565.htm</td><td>韩三平</td><td>
韩三平，1953年10月生于四川旺苍县，中国制片人、导演，原中国电影集团公司董事长。毕业于四川大学中文系[1] 
。1977年进入四川峨嵋电影制片厂，先后任照明工、场记、副导演、艺术中心主任。1983年到北京电影学院导演系进修班学习，毕业后回到峨嵋电影制片厂，任导演、副厂长。1987年，指导拍摄个人首部电影《不沉的地平线》。1991年，编剧并指导拍摄了反映毛泽东近30年的生活片断的故事片《毛泽东的故事》。1994年转任北京电影制片厂副厂长。1999年担任新成立的中国电影集团公司副董事长兼副总经理。2007年升任中影集团董事长。2009年，获2008CCTV中国经济年度人物；同年指导中华人民共和国成立60周年的献礼作品《建国大业》。2014年3月正式退休[2] 
。</td></tr></table>
