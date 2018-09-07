from urllib import request
from bs4 import BeautifulSoup
import math,pymysql,sys,re

def main():
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
    #start at 1000000 end at http code 404
    star_id = 1000000
    response = openStarPage(star_id)
    while response.getcode() != 404:
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
        insert_arr.append((star_id, soup.img['alt'], sex, soup.img['src']))
        #every 500 records insert into db
        if insert_arr.__len__() >= 500:
            insertDB(db, cursor, insert_arr)
            print("crawl at id:"+str(star_id))
        star_id += 1
        response = openStarPage(star_id)
    #if insert array has element to insert
    if insert_arr.__len__() > 0:
        insertDB(db, cursor, insert_arr)
    db.close()
    print("total star:"+str(star_id)+"    fin...")

def openStarPage(star_id):
    head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    req = request.Request("https://movie.douban.com/celebrity/"+str(star_id), headers=head)
    response = request.urlopen(req)
    return response

def insertDB(db, cursor, insert_arr):
    try:
        cursor.executemany("INSERT INTO star (star_id, star_name, sex, img_url) VALUES (%s,%s,%s,%s) \
        ON DUPLICATE KEY UPDATE star_name=VALUES(star_name),sex=VALUES(sex),img_url=VALUES(img_url)", insert_arr)
    #    db.commit()
    except Exception as e:
        print(repr(e))
        db.rollback()
    insert_arr.clear
  

if __name__ == "__main__":
    main()