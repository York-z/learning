# -*- coding:utf-8 -*-
'''
    小猪短租爬虫
    @York
    v1.1
    2019-2-19
'''
import requests
from bs4 import BeautifulSoup
from proxies import get_proxies, get_proxies_list
import re
import time
import random


def getHouseinfo(house):
    # 获取页面上房源的基本信息，返回字符串
    title = house.findAll("h4")[0].get_text().strip()
    address = house.find("span", class_="pr5").get_text().strip()
    price = house.find("div", class_="day_l").find("span").get_text().strip()
    imglink = house.find("img", id="curBigImage").attrs['src']
    lordername = house.find("a", class_="lorder_name").get_text().strip()
    if house.find("span", class_="member_boy_ico") is not None:
        lordersex = "male"
    else:
        lordersex = "female"
    houseinfo = ("\ntitle:" + title
                 + "\naddress:" + address
                 + "\nprice:¥" + price
                 + "\nimagelink:" + imglink
                 + "\nlorder_name:" + lordername
                 + "\nlorder_sex:" + lordersex)
    return houseinfo


headers = [{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" +
            " AppleWebKit/537.36 (KHTML, like Gecko) " +
            "Chrome/71.0.3578.80 Safari/537.36"},
           {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)" +
            " AppleWebKit/537.36 (KHTML, like Gecko) " +
            "Chrome/71.0.3578.80 Safari/537.36"},
           {"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8;" +
            " en-us) AppleWebKit/534.50 (KHTML, like Gecko)" +
            " Version/5.1 Safari/534.50"}]


def getLinks(url, n, proxies):
    # 获取页面上所有房源的链接并返回列表
    Linklist = []
    html = requests.get(url, headers=headers[n], proxies=proxies)
    bsObj = BeautifulSoup(html.text, 'lxml')
    for link in bsObj.findAll("a", target="_blank", href=re.compile("fangzi")):
        if 'href'in link.attrs:
            Linklist.append(link.attrs['href'])
    return Linklist


def getNextpage(url, n, proxies):
    # 获取下一页的链接
    html = requests.get(url, headers=headers[n], proxies=proxies)
    bsObj = BeautifulSoup(html.text, 'lxml')
    nextpage = bsObj.findAll(
        "a", class_="font_st", target="_self")[-1].attrs['href']
    return nextpage


def main():
    page = "http://gz.xiaozhu.com"
    infolist = []
    end_page = page + "/search-duanzufang-p13-0/"
    while page is not None:
        num = 0
        n = 0
        proxies = get_proxies(num)
        for link in getLinks(page, n, proxies):
            if num < len(get_proxies_list()):
                proxies = get_proxies(num)
                num += 1
            else:
                num = 0
                continue
            html = requests.get(link, headers=headers[n], proxies=proxies)
            bsObj = BeautifulSoup(html.text, 'lxml')
            info = getHouseinfo(bsObj)
            if info not in infolist:
                infolist.append(info)
                print(len(infolist))
                print(proxies['https'])
                print(info)
            time.sleep(2)
            n = random.randint(0, 2)
        else:
            page = getNextpage(page, n, proxies)
        if page == end_page:
            print('爬取结束')
            break


if __name__ == '__main__':
    main()
