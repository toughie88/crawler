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
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n　　",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()