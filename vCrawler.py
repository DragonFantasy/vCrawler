from urllib import request
from bs4 import BeautifulSoup
import math
import pymysql

config = {
    'host':'115.28.168.166',
    'port':3306,
    'user':'axlk',
    'password':'axlk123',
    'db':'filmstar',
    'charset':'utf8',
    'cursorclass':pymysql.cursors.DictCursor,
}
db = pymysql.connect(**config)
cursor = db.cursor()
insert_arr = []
for i in range(1000000,1000002):
    response = request.urlopen("https://movie.douban.com/celebrity/"+str(i))
    soup = BeautifulSoup(response)
    print(soup.img['alt'])
    insert_arr.append((i, soup.img['alt'], soup.img['src']))
try:
    cursor.executemany("INSERT INTO star (star_id, star_name, img_url) values (%s,%s,%s)", insert_arr)
    db.commit()
except:
    db.rollback()
db.close()
print("fin...")