# encoding:utf8
import requests
from bs4 import BeautifulSoup
import mysql.connector

config={
        'host':'127.0.0.1',#默认127.0.0.1
        'user':'root',
        'password':'root',
        'port':3306 ,#默认即为3306
        'database':'ustcGrad2015'
        }

config2={
        'host':'57c6dcec2389c.sh.cdb.myqcloud.com',
        'user':'root',
        'password':'hongqing1995',
        'port':3466 ,#默认即为3306
        'database':'test'
        }

def connDB(config_data):
    try:
        cnn=mysql.connector.connect(**config_data)
        if cnn:
            print 'ok'
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
    cursor=cnn.cursor()
    return cnn, cursor

def insertDB(cnn, cursor, examId, cardId, name, school):
    try:
        sql_query='select * from studentInfo'
        sql_insert = 'insert into studentInfo values(%s, %s, %s, %s)'
        i_data = (examId, cardId, name, school)
        cursor.execute(sql_insert, i_data)
        cnn.commit()

        cursor.execute(sql_query)
        # print cursor.fetchall()
        for cardId in cursor:
            print cardId[3]
    except mysql.connector.Error as e:
        print('query error!{}'.format(e))
    # finally:
        # cursor.close()
        # cnn.close()

def getExcel(url):
    res = requests.get(url)
    res.encoding = 'gb2312'
    if(res.status_code != 200):
        print "无法访问页面..."
        return
    else:
        print "正在解析..."
        html_doc = res.text
        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding = 'utf-8')
        students = soup.find_all('tr', style='height:20.1pt', limit=5)

        # 删除第一行的表头（网页中错误的使用了tr，所以手动删除
        del students[0]
        cnn, cursor=connDB(config)

        for student in students:
            stuInfo = student.find_all('span')
            insertDB(cnn, cursor, stuInfo[0].getText(), stuInfo[1].getText(), stuInfo[2].getText(), stuInfo[3].getText())
        cursor.close()
        cnn.close()

getExcel('http://gradschool.ustc.edu.cn/articles/2015/03/18.htm')
print '数据导入mysql数据库完毕....'
