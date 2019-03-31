import requests 
from bs4 import BeautifulSoup 
import operator 
from collections import Counter 

guidURL = 'https://dictionary.cambridge.org/browse/english-chinese-traditional/'

guideURLs = []
extendURLs = []

def start(url,op):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

    source_code = requests.get(url , headers=headers).text
    soup = BeautifulSoup(source_code, 'html.parser')
    #guide url
    if op==1:
        for each_text in soup.findAll('ul', {'class':'unstyled a--b a--rev'}):
            for href in each_text.findAll('a'):
                guideURLs.append(href.get('href'))
    else:#extend url
        for each_text in soup.findAll('div', {'class':"scroller scroller--style2 scroller--blur scroller--ind-r grad-trans3-pseudo js-scroller"}):
            for each in each_text.findAll('ul',{'class':'unstyled a--b a--rev'}):
                for href in each.findAll('a'):
                    extendURLs.append(href.get('href'))

if __name__ == '__main__':
    # guide url 
    for i in 'abcdefghijklmnopqrstuvwxyz':
        start(guidURL+i,1)
    # extend url
    for g in guideURLs:
        start(g,2)

    fd = open('guideURLs.txt', 'w')
    print(guideURLs,file = fd)
    fd.close()
    fd = open('extendURLs.txt', 'w')
    print(extendURLs,file = fd)
    fd.close()
