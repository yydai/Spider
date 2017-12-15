#coding=UTF-8
import requests
from lxml import etree
import os

def gethtml(target):
    req=requests.get(url=target)
    return req.text

def getpic(html):
    soup =etree.HTML(html)
    img_list=soup.xpath('//div/img/@data-original')
    img_list2 = soup.xpath('//div/img/@src')
    img_list.extend(img_list2)
    print(img_list)
    img_list = filter(lambda x: not (x.endswith('placeholder.png') or x.endswith('default_small.jpg') or 'BbsImg' not in x), img_list)
    img_list = map(lambda x: x.split('?')[0], img_list)
    print(img_list)
    i = 0
    for img_url in img_list:
       print (img_url)
       root='/Users/yingdai/workspace/hupu/'
       try:
           r = requests.get(img_url)
           with open(root+'{}.jpg'.format(i), 'wb') as f:
               f.write(r.content)
           f.close()
           print("文件保存成功")
           i += 1
       except:
           pass


def main():
    url='https://bbs.hupu.com/20950269.html'
    html=gethtml(url)
    with open('hupu.html', 'w') as f:
        f.write(html)
    f.close()
    print(getpic(html))

main()
