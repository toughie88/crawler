#encoding:utf-8
#python 3.4
import urllib
from urllib.request import Request
from urllib.request import urlopen
import re

from TiebaTools import TiebaTools


class Tieba:

    #初始化，传入基地址，是否只看楼主的参数
    def __init__(self,baseUrl,seeLZ):
        self.baseUrl = baseUrl
        #是否只看楼主标记　１　为真
        self.seeLz = '?see_lz='+str(seeLZ)
        #处理标记的工具类
        self.tool = TiebaTools()
        #需要写入的文件的文件名
        self.defaultFileName = "text"
        #写入的文件
        self.file = None
        #帖子的楼层
        self.floor = 1
    #传入页码，获取该帖子的html代码
    def getPage(self,pageNum):
        try:
            url = self.baseUrl+self.seeLz+'&pn='+str(pageNum)
            request = Request(url)
            response = urlopen(request)
            return response.read().decode('utf-8')
        #页面不存在抛出异常
        except HttpError as e:
            if hasattr(e,'reason'):
                print('连接错误，错误原因',e.reason)
                return None
    #获取贴吧的名称
    def getTiebaName(self):
        page = self.getPage(1)
        # <a class="card_title_fname" title="" href="/f?kw=%E9%AD%94%E5%85%BD%E4%B8%96%E7%95%8C&amp;ie=utf-8">魔兽世界吧</a>
        #正则表达式：<a class="card_title_fname".*?>(.*?)</a>
        pattern = re.compile('<a class="card_title_fname".*?>(.*?)</a>',re.S)
        result = re.search(pattern,page)
        if result is not None:
            return result.group(1).strip()
        else:
            return None

    #获取帖子的名称
    def getTitle(self):
        page = self.getPage(1)
        # <h3 class="core_title_txt pull-left text-overflow  " title="95年，我第一次枪钱" style="width: 416px">95年，我第一次枪钱</h3>
        # 正则表达式：<h3 class="core_title_txt pull-left text-overflow  ".*?>(.*?)</h3>
        pattern = re.compile('<h3 class="core_title_txt pull-left text-overflow  ".*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result is not None:
            return result.group(1).strip()
        else:
            return None

    # 获取帖子一共有多少页
    #<li class="l_reply_num" style="margin-left:8px">
    # <span class="red" style="margin-right:3px">241445</span>回复贴，共<span class="red">5457</span>页
    # </li>
    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            # print result.group(1)  #测试输出
            return result.group(1).strip()
        else:
            return None

    # 输入一页的页数，获取每一层楼的内容
    #<div id="post_content_15428864420" class="d_post_content j_d_post_content ">
    #<a href="http://jump.bdimg.com/safecheck/index?url=rN3wPs8te/pL4AOY0zAwhz3wi8AXlR5gsMEbyYdIw61qCvC3AVbXqX74TtkUtPO2UDnKGCKvC3MripOOA15C4U+GRIwDgEI46b99l0XyUM/jR49NyMTc/6qmUGNB+hoBkU5qZPKGhNuRyUQZNb8w9ed70f8iMzfNGfwE8AIkFo+IabGt6JV40dgN+wEP/FYc5KzoQPc43YhWZhAVR4xoKDA8Zu4mdgY0" class="ps_cb" target="_blank" onclick="$.stats.track(0, 'nlp_ps_word',{obj_name:'身为80后'});$.stats.track('Pb_content_wordner','ps_callback_statics')">
    # 身为80后</a>，我只想说，我们也不是什么好屌。</div>
    #这里“身为８０后”这一句出现了超链接，接下来还可能出现图片换行符等，后面写入的时候用工具类处理
    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        return items

    #创建并且打开文件
    def openFile(self,title):
        # 如果标题不是为None，即成功获取到标题
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultFileName + ".txt", "w+")
    #写入文件
    def writeFile(self,contents):
        for item in contents:
            item = "第"+str(self.floor)+"楼－－－－－－－－－－－－－－－－－－－－－" \
                             "－－－－－－－－－－－－－－－－－－－－－－－－－－－－\n"+"  "+self.tool.replace(item)+"\n"
            self.floor+=1
            self.file.write(item)

    def start(self):
        #某一页的内容
        indexPage = self.getPage(1)
        #贴吧的名称
        tiebaName = tieba.getTiebaName()
        #帖子总共有多少页
        pageNum = self.getPageNum()
        #帖子的名称
        title = self.getTitle()
        #打开文件
        self.openFile(title)
        if pageNum == None:
            print("URL已失效，请重试")
            return None
        try:
            print("贴吧名称：",tiebaName )
            print("帖子名称",title)
            print("该帖子共有" + str(pageNum) + "页")
            print("正在写入数据,请稍等")
            bar = 0
            for i in range(1, int(pageNum) + 1):
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeFile(contents)
                if int((i/int(pageNum))*100)%5==0:
                    print(bar,"%")
                    bar+=5
        # 出现写入异常
        except IOError as e:
            print("写入异常，原因" + e.message)
        finally:
            print
            "写入任务完成"
            self.file.close()


#小说
baseUrl = "http://tieba.baidu.com/p/1286517600"

tieba = Tieba(baseUrl,1)
tieba.start()