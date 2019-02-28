# -*- coding:utf-8 -*-
'''
    小猪短租爬虫
    @author:York
    @time:2019-3-1
    @version:2.0
'''
import requests
from bs4 import BeautifulSoup
import re
import time
import pymysql

headers = {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}


def store(title, address, price, imglink, lordername, lordersex):
    # 把房源信息储存到数据库，这里要新建一个对应的表
    conn = pymysql.connect(host='127.0.0.1', user='root',
                           passwd='zyq123', db='mysql')
    cur = conn.cursor()
    try:
        cur.execute('USE scraping')
        cur.execute('INSERT INTO house (title, address, price, image, name, sex) VALUES (%s, %s, %s, %s, %s, %s)',
                    (title, address, price, imglink, lordername, lordersex))
        cur.connection.commit()
    finally:
        cur.close()
        conn.close()


def getHouseinfo(house):
    # 获取页面上房源的基本信息，储存到数据库，返回房源标题
    title = house.findAll("h4")[0].get_text().strip()
    address = house.find("span", class_="pr5").get_text().strip()
    price = house.find("div", class_="day_l").find("span").get_text().strip()
    imglink = house.find("img", id="curBigImage").attrs['src']
    lordername = house.find("a", class_="lorder_name").get_text().strip()
    if house.find("span", class_="member_boy_ico") is not None:
        lordersex = "male"
    else:
        lordersex = "female"
    store(title, address, price, imglink, lordername, lordersex)
    houseinfo = "title:" + title
    return houseinfo


def getLinks(url):
    # 获取页面上所有房源的链接并返回列表
    Linklist = []
    html = requests.get(url, headers=headers)
    bsObj = BeautifulSoup(html.text, 'lxml')
    for link in bsObj.findAll("a", target="_blank", href=re.compile("fangzi")):
        if 'href'in link.attrs:
            Linklist.append(link.attrs['href'])
    return Linklist


def getNextpage(url):
    # 获取下一页的链接
    html = requests.get(url, headers=headers)
    bsObj = BeautifulSoup(html.text, 'lxml')
    nextpage = bsObj.findAll(
        "a", class_="font_st", target="_self")[-1].attrs['href']
    return nextpage


def main():
    page = "http://gz.xiaozhu.com"
    infolist = []
    while page is not None and len(infolist) < 300:
        for link in getLinks(page):
            html = requests.get(link, headers=headers)
            bsObj = BeautifulSoup(html.text, 'lxml')
            info = getHouseinfo(bsObj)
            if info not in infolist:
                infolist.append(info)
                print('\n', len(infolist))
                print(info)
            time.sleep(1.5)
        else:
            page = getNextpage(page)
    else:
        print('爬取结束')


if __name__ == '__main__':
    main()
