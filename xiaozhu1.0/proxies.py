# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import random


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}


def get_ip_list(url):
    # 获取页面上的ip地址
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[0].text.strip() + ':' + tds[1].text.strip())
    # 检测ip可用性，移除不可用ip：（这里其实总会出问题，你移除的ip可能只是暂时不能用，剩下的ip使用一次后可能之后也未必能用）
    for ip in ip_list:
        try:
            proxy_host = "https://" + ip
            proxy_temp = {"https": proxy_host}
            res = urlopen(url, proxies=proxy_temp).read()
        except:
            ip_list.remove(ip)
            continue
    return ip_list


def get_proxies(num):
    # 从储存处获取一个ip
    proxies_list = []
    with open('proxies.txt', 'r') as f:
        for ip in f.readlines():
            proxies_list.append(eval(ip.strip()))
        proxies = proxies_list[num]
    return proxies


def get_proxies_list():
    # 从储存处获取ip列表
    proxies_list = []
    with open('proxies.txt', 'r') as f:
        for ip in f.readlines():
            proxies_list.append(eval(ip.strip()))
    return proxies_list


def get_random_ip():
    proxies_list = []
    with open('proxies.txt', 'r') as f:
        for ip in f.readlines():
            proxies_list.append(eval(ip.strip()))
        proxies = random.choice(proxies_list)
    return proxies


def save_list(ip_list):
    # 把获取的ip地址存起来
    with open('proxies.txt', 'a') as f:
        for ip in ip_list:
            proxies = str({'https': 'https://' + ip}) + '\n'
            f.write(proxies)


def main():
    # 先储存ip列表以备使用
    for num in range(1, 31):
        url = 'http://www.89ip.cn/index_{}.html'.format(num)
        ip_list = get_ip_list(url)
        save_list(ip_list)


if __name__ == '__main__':
    main()
