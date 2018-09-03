from urllib import request
from bs4 import BeautifulSoup
import math

for i in range(1000000,1000020):
    response = request.urlopen("https://movie.douban.com/celebrity/"+str(i))
    soup = BeautifulSoup(response)
    print(soup.img['src'])
