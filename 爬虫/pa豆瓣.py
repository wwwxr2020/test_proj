# File: 爬虫  pa豆瓣
# @Time: 2021/11/15 21:04
import re
import urllib.request
from bs4 import BeautifulSoup
import xlwt
import pymysql
import time


# 影片链接规则
findlink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则
# 影片图片规则
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)
# 影片片名规则
findTitles = re.compile(r'<span class="title">(.*)</span>')
# 影片评分规则
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 影片评价人数规则
findNum = re.compile(r'<span>(\d*)人评价</span>')
# 影片概况规则
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 影片相关内容规则
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):      # 调用获取页面信息的函数10次
        url = baseurl + str(i*25)
        html = askURL(url)     # 保存获取到的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div",class_="item"):  # 查找符合要求的字符串，形成列表
            # print(type(item))
            item = str(item)  # 将bs4.element.Tag数据类型转换成字符串进行正则
            data = []

            # 获取影片详细链接
            link = re.findall(findlink,item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)

            imgsrc = re.findall(findImgSrc,item)[0]
            data.append(imgsrc)

            titles = re.findall(findTitles, item)
            if(len(titles)==2):
                ctitle = titles[0]
                data.append(ctitle)  # 添加中文名
                otitle = titles[1].replace("/","")
                data.append(otitle)  # 添加外文名
            else:
                data.append(titles[0])
                data.append(" ")  # 外文名留空

            rating = re.findall(findRating,item)[0]
            data.append(rating)

            num = re.findall(findNum,item)[0]
            data.append(num)

            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")  # 概述不存在留空

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)  # 去掉<br/>
            bd = re.sub('/'," ",bd)  # 替换/
            data.append(bd.strip())  # 去掉前后空格

            datalist.append(data)  # 把处理好的一部信息存储

    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    # 用户代理，告诉豆瓣服务器，我们是什么类型的机器 模拟浏览器头部信息，向豆瓣服务器发送信息
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 "
                         "Safari/537.36 Edg/95.0.1020.53"}
    request = urllib.request.Request(url,headers=head)

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html


# 保存数据
# def saveData(datalist,savepath):
#     print('Save...')
#     book = xlwt.Workbook('encoding=utf-8',style_compression=0)
#     sheet = book.add_sheet('豆瓣电影TOP250',cell_overwrite_ok=True)
#     col = ('电影详细链接','图片','影片中文名','影片外文名','评分','评价数','概况','相关信息')
#     for i in range(0,8):
#         sheet.write(0,i,col[i])
#     for i in range(0,250):
#         print("第%d条"%(i+1))
#         data = datalist[i]
#         for j in range(0,8):
#             sheet.write(i+1,j,data[j])
#     book.save(savepath)


def SaveDataDB(datalist,schema,table):
    # 创建连接
    conn = pymysql.connect(host='localhost',  # 连接名称，默认127.0.0.1
                           user='root',  # 用户名
                           passwd='020512',  # 密码
                           port=3306,  # 端口，默认为3306
                           # db=schema,  # 数据库名称
                           charset='utf8'  # 字符编码
                           )
    cur = conn.cursor()  # 创建游标
    cur.execute('DROP DATABASE IF EXISTS %s' % schema)
    cur.execute('CREATE DATABASE IF NOT EXISTS %s' % schema)
    conn.select_db(schema)
    cur.execute('DROP TABLE IF EXISTS %s' % table)
    sql1 = """
    create table douban_top250_data
    (电影链接 text,
    图片链接 text,
    电影中文名 text,
    电影外国名 text,
    影片评分 text,
    影片评价人数 text,
    影片概况 text,
    影片相关 text)"""
    sql2 = """
    insert into douban_top250_data values(%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(sql1)
    conn.commit()
    for data in datalist:
        cur.execute(sql2,data)
        conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getData(baseurl)
    # savepath = "豆瓣电影top250.xls"
    # 3.保存数据
    # saveData(datalist,savepath)
    DBschema = "spider"
    DBtable = "douban_top250_data"
    SaveDataDB(datalist,DBschema,DBtable)
    print("爬取完毕！")