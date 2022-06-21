# File: 爬虫  pa哔哩哔哩
# @Time: 2021/11/23 16:43

import re
from bs4 import BeautifulSoup
import pymysql
import requests
import xlwt

findlink = re.compile(r'<a href="//(.*?)"')
findtitle = re.compile(r'target="_blank">(.*?)</a>')
findup = re.compile('<i class="b-icon author"></i>(.*)</span></a></div>',re.S)
finduplink = re.compile(r'</span> <a href="//(.*?)" target="_blank">')
findbfl = re.compile('<i class="b-icon play"></i>(.*?)</span>',re.S)
finddml = re.compile('<i class="b-icon view"></i>(.*?)</span>',re.S)
findscore = re.compile('<div class="pts"><div>(.*?)</div>综合得分',re.S)

def askURL(url):
    # 用户代理，告诉豆瓣服务器，我们是什么类型的机器 模拟浏览器头部信息，向豆瓣服务器发送信息
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 "
                         "Safari/537.36 Edg/95.0.1020.53"}
    response = requests.get(url, headers=head)
    # html = response.content.decode("utf-8")  #bytes类型
    html = response.text.encode("utf-8")  # str类型 取文本，可以通过r.text 取图片，文件，通过r.content
    return html


def getData(html):
    datalist = []
    # 2.逐一解析数据
    soup = BeautifulSoup(html,"html.parser")
    for item in soup.find_all("div",class_="content"):  # 查找符合要求的字符串，形成列表
        item = str(item)  # 将bs4.element.Tag数据类型转换成字符串进行正则
        # print(item)
        data = []
        # 获取影片详细链接
        link = re.findall(findlink,item)  # re库用来通过正则表达式查找指定的字符串
        data.append(link[0])

        ftitle = re.findall(findtitle, item)
        data.append(ftitle[1])


        fup = re.findall(findup, item)
        fup =  re.sub(r'\n',"",fup[0]).strip(" ")
        data.append(fup)

        uplink = re.findall(finduplink,item)
        data.append(uplink[0])

        bofangliang = re.findall(findbfl, item)
        bofangliang = re.sub(r'\n', "", bofangliang[0]).strip(" ")
        data.append(bofangliang)

        danmuliang = re.findall(finddml, item)
        danmuliang = re.sub(r'\n', "", danmuliang[0]).strip(" ")
        data.append(danmuliang)

        score = re.findall(findscore,item)
        data.append(score[0])

        datalist.append(data)  # 把处理好的一部信息存储
    return datalist


# xls保存
def saveData(datalist,savepath):
    print('Save...')
    book = xlwt.Workbook('encoding=utf-8',style_compression=0)
    sheet = book.add_sheet('bilibili_top100',cell_overwrite_ok=True)
    col = ('视频链接','视频标题','up博主id','up主链接','总播放量','总弹幕量','综合评分')
    for i in range(0,7):
        sheet.write(0,i,col[i])
    for i in range(0,100):
        data = datalist[i]
        for j in range(0,7):
            sheet.write(i+1,j,data[j])
    book.save(savepath)


# mysql保存
def DBSaveData(datalist,table):
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='020512',
                          port=3306,
                          database='spider',
                          charset='utf8')
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS %s' % table)
    sql1 = """
        create table bilibili_top100_data
        (排名 int primary key not null auto_increment,
        视频链接 text,
        视频标题 text,
        up博主id text,
        up主链接 text,
        总播放量 text,
        总弹幕量 text,
        综合评分 text)"""
    sql2 = """
        insert into bilibili_top100_data (`视频链接`,`视频标题`,`up博主id`,`up主链接`,`总播放量`,`总弹幕量`,`综合评分`) values(%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(sql1)
    con.commit()
    for data in datalist:
        cur.execute(sql2, data)
        con.commit()
    cur.close()
    con.close()


if __name__ == "__main__":
    baseurl = 'https://www.bilibili.com/v/popular/rank/all'
    html = askURL(baseurl)
    datalist = getData(html)
    print("爬取完毕")
    savepath = 'bilibili_top100.xls'
    saveData(datalist,savepath)
    print("生成表格完毕")
    DBtable = "bilibili_top100_data"
    DBSaveData(datalist,DBtable)
    print("入库完毕")