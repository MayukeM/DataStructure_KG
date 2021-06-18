import pymysql
import os

"""
将csv文件数据保存到数据库
"""
def create(name_path, sql):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='study_kg')  # db:表示数据库名称
    # sql = 'insert cate (first, second, third, forth, fifth, sixth, func)VALUES (%s, %s, %s, %s, %s, %s, %s)'

    getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    getpath = ('/').join(getpath.split('\\'))
    with open(getpath + name_path, 'r') as f:
        for line in f.readlines():
            data = line.strip("\n").split(",")
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
    conn.close()
    return

if __name__ == "__main__":
    cate_path = '/kg_data/cate.csv'
    cate_sql = 'insert cate (first, second, third, forth, fifth, sixth, func)VALUES (%s, %s, %s, %s, %s, %s, %s)'
    relation_path = '/kg_data/relation.csv'
    relation_sql = 'insert relation (e1, e2, rel)VALUES (%s, %s, %s)'
    cate_rel_path = '/raw_data/relation.csv'
    cate_rel_sql = 'insert cate_rel (e1, e2, rel, c1, c2)VALUES (%s, %s, %s, %s, %s)'
    # create(cate_path, cate_sql)
    # create(relation_path, relation_sql)
    # create(cate_rel_path, cate_rel_sql)
