from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import re
import time
from fuzzywuzzy import fuzz
from bloom_filter import BloomFilter


bloombloom = BloomFilter(max_elements=10000, error_rate=0.1)

def read():
    id = 0
    with open("datatotaltest",mode="r+",encoding="utf-8") as f:
        for line in f.readlines():
             dic = {}
             line = line.rstrip("\n").lstrip(" ")
             list = line.split(" ")
             dic['分类'] = list[0]
             dic['岗位'] = list[1]
             info[id] = dic
             id += 1

def get_one_page(url,headers):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code ==200:
            return response.text
    except RequestException:
        return None
def parse_one_page(html):
    global item,flag,id,info
    soup = BeautifulSoup(html, 'lxml')
    flagdiv = soup.find_all('div',class_='empty-tip-mod')
    lis = soup.find_all('li', class_='clearfix')
    if(len(flagdiv) != 0):
        flag = False
        return ""

    for li in lis:
        dic = {}
        info1 = li.find('div', class_='reco-job-cont')
        ainfo = info1.find_all('a')
        s1 =  'https://www.nowcoder.com'+ainfo[0]['href']
        if s1 not in bloombloom:
            print("此url不存在")
            list = sort(ainfo[0].get_text())
            predict = Count(list)
            # print("预测类型：",predict)
            dic['分类'] = predict
            dic['岗位'] = ainfo[0].get_text()
            dic['公司'] = ainfo[1].get_text()
            info2 = li.find('div', class_='reco-job-info')
            info2 = info2.find('div')
            spaninfo = info2.find_all('span')
            dic['地点'] = spaninfo[0].get_text()
            dic['薪资'] = spaninfo[1].get_text()
            dic['url'] = 'https://www.nowcoder.com'+ainfo[0]['href']
            dic['存储时间'] =time.strftime("%Y-%m-%d")
            # dic['附加信息']
            item[id] = dic
            id += 1
            bloombloom.add(dic['url'])
        else:
            print("此url存在")
def sort(text):
    print(text)
    list = []
    for v in info.values():
        smalldic = {}
        score = fuzz.token_sort_ratio(text,v['岗位'])
        smalldic['分类'] = v['分类']
        smalldic['岗位'] = v['岗位']
        smalldic['相似度'] = score
        list.append(smalldic)
    list.sort(key=f1)
    list.reverse()
    # print(list)
    return list[0:10]
    # 以某个特征
def f1(x):
    return x['相似度']


#选取k个数，并计算k个数的类别概率
def Count(list):
    # print(list)
    kinddic = {"产品":0,"前端":0,"测试":0,"研发":0,"算法":0,"运营":0,"数据":0}
    for i in range(len(list)):
        kinddic[list[i]['分类']] += (10 - i)
    # print(kinddic)
    max_prices = max(zip(kinddic.values(), kinddic.keys()))
    return max_prices[1]


def store():
    global item
    with open("olddata",mode="a",encoding="utf-8") as f:
        for v in item.values():
            for value in v.values():
                f.write(value+" ")
            f.write("\n")
    item = {}
def main():
    # confine = 1000
    # total = 0
    read()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.The Younger Generation In the Twenty-first Century; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    headurl = 'https://www.nowcoder.com/job/center?page='
    i = 1
    while flag:
        url = headurl + str(i)
        # url = headurl
        print(url)
        #获取源码
        html = get_one_page(url,headers)
        #解析源码
        parse_one_page(html)
        i += 1
        store()
    #统计功能
    # print(item)

if __name__ == '__main__':
    flag = True
    id = 0
    info = {}
    item = {}
    main()