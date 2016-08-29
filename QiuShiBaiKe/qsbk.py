# encoding:utf-8
# python 2.7
# 参考页面　http://cuiqingcai.com/990.html
import re
import urllib2
import thread


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0"
        self.Host = "www.qiushibaike.com"
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent,
                        'Host': self.Host
                        }
        # 存放段子的变量，每一个元素是每一页的段子
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = "http://www.qiushibaike.com/hot/page/" + str(pageIndex)
            # 构建请求的requset
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            # 将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"链接失败,错误原因", e.reason
                return None

    # 传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)

        if pageCode is None:
            print "页面加载失败"
            return None

        # 获取内容：发布人，段子内容，点赞个数,评论个数
        pattern = re.compile(
            '<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>.*?<i class="number">(.*?)</i>',
            re.S)
        items = re.findall(pattern, pageCode)
        # 存放每页的段子
        pageStories = []
        for item in items:
            pageStories.append([item[0].strip(), item[1].strip(), item[2].strip(), item[3].strip()])
        return pageStories

    # 加载并提取页面的内容，加入到列表中
    def loadPage(self):
        # 如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                # 获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                # 将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    # 调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            # 等待用户输入
            input = raw_input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            # 如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            #按顺序：发布人，段子内容，点赞个数,评论个数
            print u"第%d页\t发布人:%s\t赞:%s\t评论数:%s\t段子内容:%s\n" % (page, story[0], story[2], story[3], story[1])

    # 开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出(也就是删除一页)
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories, nowPage)


spider = QSBK()
spider.start()



