# File: test_proj  sql_use
# @Time: 2022/6/23 1:11
from  MYSQL_link import *

db = 'polls'
# 数据层面
## 插入数据
sql1 = """insert into polls_choice (choice_text,votes,question_id) values('Test',5,1)"""
# 结构层面

sql_link_crud(db, sql1)