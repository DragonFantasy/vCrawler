from urllib import request
from bs4 import BeautifulSoup
import math,pymysql,sys,re

config = {
    'host':'115.28.168.166',
    'port':3306,
    'user':sys.argv[1],
    'password':sys.argv[2],
    'db':'filmstar',
    'charset':'utf8',
    'cursorclass':pymysql.cursors.DictCursor,
}
db = pymysql.connect(**config)
cursor = db.cursor()
insert_arr = []
for i in range(1000000,1000002):
    response = request.urlopen("https://movie.douban.com/celebrity/"+str(i))
    soup = BeautifulSoup(response, features="html.parser")
    info_list = soup.select(".info")
    sex = 0
    for info in info_list:
        li_list = info.find_all('li')
        for li in li_list:
            if "性别" in str(li):
                if("男" in str(li)):
                    sex = 1
                break
    insert_arr.append((i, soup.img['alt'], sex, soup.img['src']))
try:
    cursor.executemany("INSERT INTO star (star_id, star_name, sex, img_url) VALUES (%s,%s,%s,%s) \
     ON DUPLICATE KEY UPDATE star_name=VALUES(star_name),sex=VALUES(sex),img_url=VALUES(img_url)", insert_arr)
    print(cursor)
    db.commit()
except Exception as e:
    print(repr(e))
    db.rollback()
db.close()
print("fin...")