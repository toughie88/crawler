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

        return res_data