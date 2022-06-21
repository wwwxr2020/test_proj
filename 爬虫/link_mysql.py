# *-* coding:utf8 *-*
# File: 爬虫  T链接数据库
# @Time: 2021/11/9 16:01

import pymysql
#连接数据库
conn=pymysql.connect(host = 'localhost', # 连接名称，默认127.0.0.1
user = 'root', # 用户名
passwd='020512', # 密码
port= 3306, # 端口，默认为3306
#db='test_db1', # 数据库名称
charset='utf8' # 字符编码
                     )
cur = conn.cursor() # 生成游标对象

try:

    DB_NAME = 'movie'
    cur.execute('DROP DATABASE IF EXISTS %s' %DB_NAME)
    cur.execute('CREATE DATABASE IF NOT EXISTS %s' %DB_NAME)
    conn.select_db(DB_NAME)

    sql1 = """
    create table douban_data
    (电影链接 text,
    图片链接 text,
    电影中文名 text,
    电影外国名 text,
    影片评分 text,
    影片评价人数 text,
    影片概况 text,
    影片相关 text)"""
    cur.execute(sql1)
    conn.commit()

# #创建表
#     TABLE_NAME = 'bankData'
#     cur.execute('CREATE TABLE %s(id int primary key,money int(30))' %TABLE_NAME)
#
# # 批量插入纪录
#     values = []
#     for i in range(20):
#         values.append((int(i),int(2*i)))
#     cur.executemany('INSERT INTO bankData values(%s,%s)',values)
#     conn.commit()
#     # 查询数据条目
#     count = cur.execute('SELECT * FROM %s' %TABLE_NAME)
#     print ('total records:{}'.format(cur.rowcount))
#
#     # 获取表名信息
#     desc = cur.description
#     print ("%s %3s" % (desc[0][0], desc[1][0]))
#
#     cur.scroll(1,mode='absolute')
#     results = cur.fetchall()
#     for result in results:
#         print (result)

except:
    import traceback
    traceback.print_exc()
    # 发生错误时会滚
    conn.rollback()
finally:
    # 关闭游标连接
    cur.close()
    # 关闭数据库连接
    conn.close()
