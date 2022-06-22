# File: test_proj  MYSQL_link
# @Time: 2022/6/23 0:22

import pymysql


def sql_link_crud(db, *args):
    # pymysql链接mysql
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='12345678',
                          port=3306,
                          charset='utf8')
    cur = con.cursor()
    con.select_db(db)
    for sql in args:
        try:
            cur.execute(sql)
            con.commit()
        except:
            # 发生错误会回滚
            con.rollback()
    cur.close()
    con.close()
