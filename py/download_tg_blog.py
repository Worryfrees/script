#!/usr/bin/env python3
"""
可以爬取https://telegra.ph 这个博客中的图片
支持多线程下载图片，目前测试是单线程的10倍速度
"""
import re, os
import time

import bs4, requests, random
import threading


# 设置伪装ip
def random_ip():
    a = random.randint(1, 255)
    b = random.randint(1, 255)
    c = random.randint(1, 255)
    d = random.randint(1, 255)
    return str(a) + "." + str(b) + "." + str(c) + "." + str(d)


# 获取到链接列表
def picture_list(tg_url):
    source_url = tg_url
    agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92."
                           "0.4515.107 Safari/537.36",
             "X-Forwarded-For": random_ip()
             }
    get_url = requests.get(source_url, headers=agent)
    response = get_url.content.decode()
    get_url.close()
    soup = bs4.BeautifulSoup(response, "html.parser")
    x = soup.find_all("img")
    title = soup.find("title").string
    return x, title


# 提取列表中的链接,返回一个可以迭代的对象
def get_img_object(url):
    try:
        for i in url:
            i = str(i)
            regex = re.findall(r"(/file/.*.jpg)", i)
            img_list_url = "https://telegra.ph" + regex[0]
            yield img_list_url
    except Exception:
        print("链接有错误，跳过")


def get_img_list(object_):
    list_of_spaces = []
    for list_ in object_:
        list_of_spaces.append(list_)
    return list_of_spaces


def download(url_list, title):
    # 循环下载
    for url in url_list:
        agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92."
                               "0.4515.107 Safari/537.36",
                 "X-Forwarded-For": random_ip()
                 }
        get = requests.get(url, headers=agent)
        response = get.content
        get.close()
        filename = url.split("/")[-1]
        with open(f"./download_img/{title}/{filename}", "wb+", buffering=2048) as f:
            f.write(response)


def run():
    num = 50
    for tg_url in open("url.txt", "r", encoding="utf-8"):
        # tg_url = input("输入tg博客的链接：")
        x, title = picture_list(tg_url)  # 传入url解析获得一个带a标签的图片链接列表
        img_list = get_img_object(x)  # 提取列表中所有的链接，返回一个可以迭代的object
        url_list = get_img_list(img_list)  # 把对象中的链接迭代出来，转换成一个列表再返回

        # 列表表达式，把一个大的列表，分割为每5个值一个的列表
        list_5 = [url_list[i:i + num] for i in range(0, len(url_list), num)]
        try:
            os.makedirs("download_img/{}".format(title))
        except Exception:
            print("文件夹存在")
            continue
        # 限制线程创建
        time.sleep(2)
        for url in list_5:
            t = threading.Thread(target=download, args=(url, title,))
            t.start()
        num_img = len(url_list)
        print("总共有{}张图片".format(num_img))
        print("开始下载")


if __name__ == "__main__":
    run()
