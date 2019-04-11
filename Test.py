# -*- coding: utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import csv

def write_to_file(content):
    with open('result_bs4.csv', 'w') as csvfile:
        headers = ['序号', '房子详情Url', '标题', '地区名', '房子图片', '价格', '出租类型', '房型', '面积', '上架时间',
                   '朝向', '联系人', '联系号码', '基础信息', '设施', '房源介绍']
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(content)
        csvfile.close()
def getDetail(url):
    soup = BeautifulSoup(request.urlopen(url).read(), features="lxml")
    # print(soup.prettify())
    imgs = []
    for item in soup.find(class_="content__article__slide--small content__article__slide_dot").find_all('li'):
        imgs.append(str(item.contents[1]['src']).replace("126x86", "780x439"))
    price = soup.find(class_="content__aside--title").span.contents[0]
    rentMode = soup.find(class_="house").find_parent("span").contents[1]
    houseType =soup.find(class_="typ").find_parent("span").contents[1]
    area = soup.find(class_="area").find_parent("span").contents[1]
    arriveTime = soup.find(class_="content__subtitle").contents[2]
    orientations = soup.find(class_="orient").find_parent("span").contents[1]
    contactName = soup.find(class_="name").contents[0]
    contactTelephone = soup.find(class_="phone").contents[0]
    BasticInfo1 = soup.find_all(class_="fl oneline")
    BasticInfo = []
    for i in range(1, len(BasticInfo1)):
        if i % 3 != 0:
            BasticInfo.append(BasticInfo1[i].contents)
    facilities = []
    items = soup.find(class_="content__article__info2").find_all("li")
    for i in range(1, len(items)):
        facilities.append(items[i].contents[1])
    introduce1 = soup.find(class_="content__article__info3").find_all("p")
    introduce = ""
    if len(introduce1) > 0:
        for i in range(len(introduce1[1].contents)):
            if( i%2==0 ):
                introduce += str(introduce1[1].contents[i])
    row = ['house'+str(len(rows)+1), houseUrl, title, realmName, imgs, price, rentMode, houseType, area, arriveTime,  orientations, contactName, contactTelephone, BasticInfo, facilities, introduce]
    rows.append(row)


class House:
    houseUrl = ""
    title = ""
    realmName = ""


url = "https://bj.lianjia.com/zufang/pg1/" #网页地址
wp = request.urlopen(url) #打开连接
content = wp.read() #获取页面内容
soup = BeautifulSoup(content, features="lxml")
rows = []
for item in soup.select('div > .content__list--item'):
    prefix = "https://bj.lianjia.com"
    houseUrl = prefix+item.find(class_="content__list--item--aside")["href"]
    title = item.find(class_="content__list--item--title twoline").a.contents[0]
    realmName = ""
    for item1 in item.find(class_="content__list--item--des").find_all("a"):
        realmName += item1.contents.pop(0)+" "
    getDetail(houseUrl)
    write_to_file(rows)

