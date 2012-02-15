import pymysql

class Database(object):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='feel')
        conn.autocommit(1)
        cursor = conn.cursor()

    
