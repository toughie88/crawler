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