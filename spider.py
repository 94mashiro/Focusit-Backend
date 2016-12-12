from bs4 import BeautifulSoup
from mongoengine import *
import requests
import datetime
import time
import json
import utils
import classes

connect('Articles', host='127.0.0.1', port=27017)

sg_headers = {
    'Host': 'segmentfault.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://segmentfault.com/news/newest',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
}

gold_headers = {
    'Host':'api.leancloud.cn',
    'Connection':'keep-alive',
    'X-LC-UA':'AV/js1.5.0',
    'Origin':'https://gold.xitu.io',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
    'Content-Type':'application/json;charset=UTF-8',
    'X-LC-Sign':'cbec2ebcb163f668fcf2026b349758cc,1481531000384',
    'X-LC-Id':'mhke0kuv33myn4t4ghuid4oq2hjj12li374hvcif202y5bm6',
    'Accept':'*/*',
    'Referer':'https://gold.xitu.io/welcome',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6'
}



# base_url = 'https://segmentfault.com'
# html_doc = requests.get('https://segmentfault.com/news/newest').text
# soup = BeautifulSoup(html_doc,"html.parser")
#
# titles = soup.find_all("h4",{"class":"news__item-title"})
#
# authors = soup.find_all("p",{"class":"news__item-meta"})
#
# links = soup.find_all("h4",{"class":"news__item-title"})
#
# for idx in range(0,len(titles)):
#     title = titles[idx].a.string
#     author = authors[idx].span.a.string
#     link = links[idx].a.get('href')

def segmenfault_spider():
    base_url = 'https://segmentfault.com'
    for i in range(1,2):
        html = requests.get('https://segmentfault.com/news/newest?page=%i'%i , headers=sg_headers).text
        soup = BeautifulSoup(html,"html.parser")
        origin = 'segmentfault'
        titles = soup.find_all("h4",{"class":"news__item-title"})
        authors = soup.find_all("p",{"class":"news__item-meta"})
        links = soup.find_all("h4",{"class":"news__item-title"})
        tags = soup.find_all("a",{"class":"ml10"})
        tags = tags[1:len(tags)+1]
        for idx in range(0,len(titles)):
            title = titles[idx].a.string
            author = authors[idx].span.a.string
            url = links[idx].a.get('href')
            tag = []
            tag.append(tags[idx].string)
            classes.Article(title=title,author=author,url=url,tag=tag,origin=origin,createdAt=datetime.datetime.now()).save()
        print('Page %i end.' % i)
    print('sf mission success')

def gold_spider():
    html = requests.get('https://api.leancloud.cn/1.1/classes/Entry?&where=%7B%7D&include=user&limit=20&skip=0&order=-hotIndex',headers=gold_headers).text
    results = json.loads(html)['results']
    for i in range(0,len(results)):
        data = json.loads(html)['results']
        title = data[i]['title']
        url = data[i]['url']
        tag = data[i]['tagsTitleArray']
        origin = 'gold'
        author = data[i]['user']['username']
        createdAt = data[i]['createdAt']
        createdAt = utils.stringToDateTime(createdAt[0:len(createdAt)-5])
        classes.Article(title=title,author=author,url=url,tag=tag,origin=origin,createdAt=createdAt).save()
        print('Article %i end.' % i)
    print('gold mission success')

if __name__ == '__main__':
    segmenfault_spider()
    gold_spider()
