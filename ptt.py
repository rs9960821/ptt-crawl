import requests
import re
import csv
from bs4 import BeautifulSoup

class spider():
    def __init__(self):
        self.baseurl = "https://www.ptt.cc/bbs/"
        self.headers = {"User-Agent":"Mozilla/5.0"}
        #與系統告知已滿18歲
        self.cookies = {'over18': '1'}
        self.page = 1
        self.page2 = 1
        self.i = 0
        
    def getPage(self, url):
        res = requests.get(url, headers = self.headers, cookies = self.cookies)
        res.encoding = "utf-8"
        html = res.text
        self.pares(html)
        
    def writeData(self, L_list):  
        if self.page2 == 1:
            with open('ptt.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(['標題', '網址'])
        try:
            for r_tuple in L_list:
                # print(r_tuple)      
                with open('ptt.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(r_tuple)
            with open('ptt.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(["page", str(self.page2)])
                self.page2 += 1
                print('Loading success', 'Page', self.i)
        except UnicodeEncodeError:
            print('loading fail', 'Page', self.i)
            print('encoding is abnormal')
                
    def pares(self, html):
        s = re.compile('<a href=.*?.html">(.*?)</a>', re.S)
        a = re.compile('<a href="(.*?)">.*?</a>', re.S)
        r_list = s.findall(html)
        t_list = a.findall(html)
        L_list = []
        L_list = [[i]+['https://www.ptt.cc'+j] for i, j in zip(r_list, t_list)]
        # print(L_list)
        self.writeData(L_list)
        
    def work(self):
        # url = self.baseurl + "index.html"
        url = 'https://www.ptt.cc/bbs/index.html'
        res = requests.get(url, headers = self.headers, cookies = self.cookies)
        soup = BeautifulSoup(res.text, 'lxml')
        alist = []
        blist = []
        for i in soup.select('.b-ent'):
            a = (i.select('.board-class')[0].text)
            b = (i.select('.board-name')[0].text)
            alist.append(a)
            blist.append(b)  
        #搜尋匹配看板
        name = input('Want to search class:')
        for x in range(128):
            if name == alist[x]:
                code = blist[x]
                url2 = self.baseurl + str(code)
                break
        else :
            print('無此看板')
            self.work()

        key = int(input('Want to search pages:'))
        while self.i < key:
            url = url2 + "/index" + str(self.page) + ".html"
            self.page += 1
            self.i += 1
            self.getPage(url)
        print("Search done")
        print("Thank you, Bye")
            
            
if __name__ == "__main__":
    spider = spider()
    spider.work()

