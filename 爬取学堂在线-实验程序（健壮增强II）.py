# -*- coding:utf-8 -*-

# 【导入库】：导入相关库函数
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from urllib import parse
import pymysql.cursors

page_num = 2

for num in range(page_num):
    url = 'http://www.xuetangx.com/courses?credential=0&page_type=0&cid=0&process=0&org=0&course_mode=0&page=' + str(num)
    req = Request(url)
    postData = parse.urlencode([
        ("credential", "0"),
        ("page_type", "0"),
        ("cid", "0"),
        ("process", "0"),
        ("org", "0"),
        ("course_mode", "0"),
        ("page", str(num))
    ])
    req.add_header("Host", "www.xuetangx.com")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
    resp = urlopen(req, data=postData.encode("utf-8"))

    soup = BeautifulSoup(resp, 'html5lib')
    course_name = soup.findAll("h2", class_="coursetitle")
    course_teacher = soup.select('div.fl.list_inner_right.cf div div.cf.teacher div.fl.name p')
    course_intro = soup.findAll("div", class_="txt_all")

    for a, b, c in zip(course_name, course_teacher, course_intro):
        a = a.get_text()
        b = b.get_text()
        c = c.get_text().replace('\n','').replace('简介','')
        # print(a, b, c)
        # 建立一个链接，需要本地安装好mysql环境，端口、用户名、密码需要自行设定
        connection = pymysql.connect(host='localhost', port=3306, user='root', passwd="root", db='test_py2mysql',charset='utf8')
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO `xuetang_course`(`course_name`,`course_teacher`,`course_info`)VALUES(%s,%s,%s)"
            cursor.execute(sql, (a, b, c))
            connection.commit()
            #results = cursor.fetchone()
            #print(results)
        finally:
            cursor.close()
            connection.close()

print("[数据库操作完成]")
