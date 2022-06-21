# File: 爬虫  bs4
# @Time: 2021/11/15 21:40

from bs4 import BeautifulSoup

file = open("./baidu.html","rb")
html = file.read().decode("utf-8")
bs = BeautifulSoup(html,"html.parser")

# # 1.Tag 标签及其内容：拿到他所找到的第一个内容
# print(bs.title)
# print(bs.title.string)
#
# # 2.NavigableString 标签里的内容（字符串）
# print(bs.a.attrs)
#
# # 3.BeautifulSoup 表示整个文档
# print(bs.a.string)
#
# # 4.Comment 是一个特殊的NavigableString，输出的内容不包含注释符号


# t_list = bs.find_all("a")
# print(t_list)
import re
t_list = bs.find_all(re.compile("a"))
print(t_list)