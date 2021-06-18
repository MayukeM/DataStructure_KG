import pymysql
import os

"""
将csv文件数据保存到数据库
"""


def cate_rel_show(sql):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='study_kg')  # db:表示数据库名称

    cursor = conn.cursor()
    cursor.execute(sql)
    sql_data = cursor.fetchall()
    sql_data = list(sql_data)
    data = []  # bootstrap table 所需要的数据
    for item in sql_data:
        d = {}
        d['cate_rel_id'] = item[0]
        d['e1'] = item[1]  # 随机选取汉字并拼接
        d['e2'] = item[2]
        d['rel'] = item[3]
        d['c1'] = item[4]
        d['c2'] = item[5]
        data.append(d)

    conn.commit()
    cursor.close()
    conn.close()

    return data


def operation(sql, item):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='study_kg')  # db:表示数据库名称
    cursor = conn.cursor()

    cursor.execute(sql, item)

    conn.commit()
    print("已提交数据库")
    cursor.close()
    conn.close()

    return
# if __name__ == "__main__":
