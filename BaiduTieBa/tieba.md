# 爬取百度贴吧上的帖子（小说）

标签（空格分隔）： 爬虫

---

## 爬取网页简介 ##
爬取的网页是本人在以前高中的时候在魔兽世界吧看的一篇小说，比较精彩：《95年，我第一次枪钱》，当时用百度贴吧显得略麻烦，最近学习了爬虫，所以今天准备用爬虫将其爬下来，存储为txt文档
百度贴吧地址：[95年，我第一次枪钱](http://tieba.baidu.com/p/1286517600?see_lz=1&pn=1)

----------

## 说明 ##

本项目参照博客：[cuiqingcai.com](http://cuiqingcai.com/993.html)

 1. 项目目的：
    - 实现对百度百科的各种帖子进行抓取
    - 实现只看楼主的功能
    - 将抓取到的内容分析并保存到本地
 2. 改版说明：
    - 在原博客中，采用python2.7编写，现在我将其改版为python3.4
    - 将部分项目功能进行精简改进，修改文件排版以及存储方式
    - 原博客中爬取的NBA吧的一篇帖子，在这里我爬取一篇小说

----------

## 分析 ##

### 抓取功能实现
观察百度贴吧帖子的url:
http://tieba.baidu.com/p/1286517600?see_lz=1&pn=1
其中see_lz和pn是该URL的两个参数，分别代表了只看楼主和帖子页码，等于1表示该条件为真。
所以将url分为两部分，第一部分为资源定位符：http://tieba.baidu.com/p/1286517600
第二部分为帖子的参数。
### 抓取内容的确定

1. 贴吧的名称，比如此处抓取的是魔兽世界吧。

```html

<a class="card_title_fname" title="" href="/f?kw=%E9%AD%94%E5%85%BD%E4%B8%96%E7%95%8C&amp;ie=utf-8">魔兽世界吧</a>
        
```

正则表达式：

```html
<a class="card_title_fname".*?>(.*?)</a>

```

２．爬取帖子的名称

```html

<h3 class="core_title_txt pull-left text-overflow  " title="95年，我第一次枪钱" style="width: 416px">95年，我第一次枪钱</h3>
        
```

正则表达式：

```html

<h3 class="core_title_txt pull-left text-overflow  ".*?>(.*?)</h3>

```

３．帖子的总页数

```html

<li class="l_reply_num" style="margin-left:8px">
 <span class="red" style="margin-right:3px">241445</span>回复贴，共<span class="red">5457</span>页
 </li>
        
```

正则表达式：

```html

<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>

```

４．楼层的内容

```html

<div id="post_content_15428864420" class="d_post_content j_d_post_content "><a　href="http://jump.bdimg.com/safecheck/index?url=rN3wPs8te/pL4AOY0zAwhz3wi8AXlR5gsMEbyYdIw61qCvC3AVbXqX74TtkUtPO2UDnKGCKvC3MripOOA15C4U+GRIwDgEI46b99l0XyUM/jR49NyMTc/6qmUGNB+hoBkU5qZPKGhNuRyUQZNb8w9ed70f8iMzfNGfwE8AIkFo+IabGt6JV40dgN+wEP/FYc5KzoQPc43YhWZhAVR4xoKDA8Zu4mdgY0" class="ps_cb" target="_blank" onclick="$.stats.track(0, 'nlp_ps_word',{obj_name:'身为80后'});$.stats.track('Pb_content_wordner','ps_callback_statics')">身为80后</a>，我只想说，我们也不是什么好屌。</div>
    
```

正则表达式：

```html

<div id="post_content_.*?>(.*?)</div>

```


----------

###　标签的处理

在帖子的内容中，出现了很多类似于图片和超链接的标签，所以专门用一个工具类对这些标签进行清除.

 １．将表格制表<td>替换为\t
 
 ２．把段落开头换为\n加空两格
 
 ３．将换行符或多换行符替换为\n
 
 ４．将其余标签剔除
 
 
 


----------
### 文件写入

创立文件利用循环一页一页的写入


----------
## 源代码 ##

１．爬虫类：teiba.py

```python

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

```

2.工具类:TiebaTools

```python

#工具类，处理页面的楼层中文字里面的标签
import re

#处理页面标签类
class TiebaTools:

    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')

    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')

    #将换行符或多换行符替换为\n
    replaceBR = re.compile('<br>.*?<br>|<br>')

    #将其余标签剔除
    removeExtraTag = ｀｀re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n　　",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

```


----------

## 运行输出 ##

运行程序大约２分钟后就能得到结果

> 贴吧名称： 魔兽世界吧
帖子名称 95年，我第一次枪钱
该帖子共有127页
正在写入数据,请稍等
0 %
5 %
10 %
15 %
20 %
25 %
30 %
35 %
40 %
45 %
50 %
55 %
60 %
65 %
70 %
75 %
80 %
85 %
90 %
95 %
100 %
Process finished with exit code 0




----------

## 输出文档 ##
 [95年，我第一次枪钱.txt](/source/95年，我第一次枪钱.txt)
 
 示例：
 

> 第1楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  身为80后，我只想说，我们也不是什么好屌。
第2楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  熬了六年，终于毕业了，最后一次招记，我和四个同学把短裤套在头上，用麻袋把体育老师照主，再扣一个啤酒箱，用砖头和皮带打了他将进五分钟。
第3楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  只因为他教我们作操时，摸了我小女朋友的胸部，我发誓，我毕业的时间一定要找回这个亏来。当时打完后，我把麻袋拿了下来，用砖头拍着他的头问他，你服不服，他没说话，可能已经被打蒙了，我又问他知道我们为什么打你吗？因为你是个老流氓！
第4楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  我们临走时把他身上的烟给抢走了。把刚刚用来套头啤酒箱卖了十元钱。我们五人抽着烟去买了四十个游戏币，当时恐龙快打和刀客哥我已经不玩了，拳皇94，95我的最爱，由其喜欢不知火舞。晃啊晃，太有味道了。
第5楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  一会就玩完了，旁边和我对打那叔叔，还挑逗我，继续来打啊，我一问同学都没币了。吗的，我们五人就出了游戏厅。这时张飞就起个好注意，咱们抢点钱回来继续玩吧，（我们五人自封五虎上将，我是黄忠，因为我最色，所以姓黄）赵云就不同意，说没听学校说吗，现在严打，抢五毛就得蹲俩年。
第6楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  我们一商量，决定还是要抢，不过要抢年纪小点的，这样恐吓下，他就不敢报警了。其实当时报警很难，没有手机，家里电话都没普及，警局也少，一个区也就一个左右。于是我们开始寻找目标。
第7楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  在游戏厅门口等了大约10来分钟，看见走过来一个黄毛。我们5个人商量了下，决定还是不要抢他的好，一般染头的都是不好惹的，黄毛用眼神瞟了我们一眼就进去了，关羽骂到：瞟你妈，再瞟挖了你的双眼，关羽喜欢天天在腰里别着一把折叠三菱刺，那时三菱刺绝对是偶像级凶器！
第8楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  又蹲了一会，看见走来一个和我们差不多大的学生，因为当时放假期间，所以都没有穿校服的，我们一看机会来了，就5个人走过去，张飞把手搭在这小孩的肩膀上，问：同学是不是去打游戏机啊，有没有钱，借点花花，我们5个人中午都没吃饭，你看咋办？然后我们就开始搜兜，小孩也不敢放声，我们搜了2元钱，就把他放了，临走时发现这小孩没有回去，而是继续走进了电游厅！
第9楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  我们也没在意，决定再继续抢点钱，2元钱根本不够玩的，就当我们还在蹲点的时候，刚刚那被抢的小孩从电游厅里走了出来，还带着那个黄毛，指着我们说：哥就是他们抢我钱！黄毛走过来，用食指指着我说：是你抢我弟钱嘛？我没敢说话，然后用食指不停点我的头，黄毛比我高快2个头的身高，两下就把我点倒了。然后转身扇了赵云2个耳光，说小B崽子就你抢钱！继续转身踹了2脚旁边的张飞，我们3个都没敢反抗，甚至也没有出声。黄毛继续转身要踹张飞旁边的关羽。然后发生了我一生最悲剧的一幕，也是我第二生命的开始！
第10楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  关羽抽出了他那折叠三菱刺，猛的捅了黄毛2刀，第一刀非常快，肠子都拽了出来，第二刀关羽没有拔出来，而是松了手，当时那黄毛他弟狂叫，是不挺的狂叫，叫声含着哭声。我们4个人全都吓傻了，我当时的感觉是腿已经站不住了，虽然经常打架，看打架，但是第一次近距离看捅人，我还是崩溃了。关羽捅完也吓傻了，这时周围的人都往这里聚了过来，游戏厅里也出来了好多人，过来的大人看见这场面都叫了出来，黄毛躺在地上，嘴里不停的吐血，手握着刀，肚子上全是血，还有被拉出的肠子！场面可以说恐怖到极点！
第11楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  不知道我们5个人谁第一个跑了，反正我看见他们都跑了，我也跟着他们跑，一直往家的方向跑！我们5个人都住的非常近，他们4个人住的是平房，而我是唯一住楼房的人。跑到我家门口，我们停住了，张飞说了句话：回家别告诉家长！然后我们就散了，这次的分离不算是永别，但也差不多了。回到家，我俩眼发直，老爸老妈还都没有下班。等到6点左右，老爸老妈都回家了，我像往常一样在家玩任天堂8位机！但是心里特别慌张！
第12楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  吃完晚饭，老妈问我，今天学校招记都讲什么了，我说什么也没讲。等下次才知道分哪个学校！晚上8点左右，有人敲门，我感觉到要倒霉了，我祈祷千万别是找我的，千万别是！但是该来的还是来了，来了3个**，还有那个被我们抢钱的小孩，身后还有好几个大人，黄毛他弟用手指着我哭着说，是他，是他，不过不是他捅的！**就把下午的惨剧跟我父母说了，我爸回头就是一拳给我打飞了，我妈气的一直拿巴掌扇我的头和脸。我当时的脑子里一直回荡着**说的话，那黄毛死了！
第13楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  民（和谐）警跟我爸说，明早你带着你孩子到局里来吧，然后这一大群人就走了。父母又是一顿暴打，然后我把今天发生的经过从头到尾说了一遍。我妈一直重复着，说你多少次了，不让你和他们在一起玩，你就不听，出事了吧，然后继续打我。后来打累了，就把我关进小屋里。我躲在小屋里听着，我父母在大屋吵架，吵的特别凶，一直吵到半夜。第二天，我看见我妈的眼睛是肿的，估计是昨天哭的。我和我父母三人就来了警局。我录了口供，然后在警局呆了一上午。我还想着能碰见他们4个人呢，结果很失望，我走出警局的时候也没有看到他们4个！
第14楼－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
  接下来的日子，我一直是被父母关在家里，被反锁在家里。虽然只有2楼，但是我也不敢跳窗出去，不是我不敢跳，而是我不敢出门，我怕被抓进监狱去。我在家里很闷，只能玩8位机，和胡思乱想，我想我们被抓肯定是游戏厅的老板告的秘，因为有次赵云他爸上游戏厅去抓赵云，和老板吵吵了起来，赵云他爸还恐吓老板，你再让学生进来玩，就把你告了！被关了大约2个星期左右，马上就要召记了，这次学校要通告分学校的事情了，因为我是非农户口。我铁定会被分到49中的，而那些农村户口的学生只能分到偏远的14中，14中是所寄宿初中学校，那里大部分是农村人和有着农村户口的城市人！

 
 




