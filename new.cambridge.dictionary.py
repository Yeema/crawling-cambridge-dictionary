#!/usr/bin/env python
# coding: utf-8

# In[11]:


from bs4 import BeautifulSoup
from collections import defaultdict
import requests


# In[10]:


def extract(soup):
    for entry in soup.select('.entry'):
        for big_block in entry.select('.entry-body__el.clrd.js-share-holder'):
            if big_block.select_one('.pos-header .headword'):
                head_word = big_block.select_one('.pos-header .headword').text
            
            pos = big_block.select_one('.pos-header .pos').text
            print('---', head_word, pos, '---')


            for block in big_block.select('.sense-block'):
                guideword = ''
                extra_sents = []
                big_sense = defaultdict(list)
                ch_def = ''
                gcs = ''
                en_def = ''


                if block.select_one('.guideword'): # guide word
                    guideword = block.select_one('.guideword').text.strip()

                if block.select('.extraexamps .eg'): # extra sents of a block
                    extra_sents = [extra_sent.text for extra_sent in block.select('.extraexamps .eg')] 


                for x in block.select('.sense-body .def-block'):
                    temp = {}

                    if x.select_one('.def-info span.epp-xref'):
                        print(x.select_one('.def-info span.epp-xref').text.strip()) # 等級
                        level = x.select_one('.def-info span.epp-xref').text.strip()
                    else:
                        print('NONE')
                        level = 'none'

                    if x.select_one('.def-info .gcs'):
    #                     print(x.select_one('.def-info .gcs').text.strip())
                        gcs = x.select_one('.def-info .gcs').text.strip()

                    if x.select_one('.def'):
                        en_def = x.select_one('.def').text.strip()
    #                 print(x.select_one('.def').text.strip())

                    if x.select_one('.trans').text:
                        ch_def = x.select_one('.trans').text.strip()

                    examples = []
                    for example in x.select('.examp.emphasized'): #例句
        #                 print(example.select_one('.eg').text)
        #                 print(example.select_one('.trans').text)
                        if example.select_one('.eg'):
                            eg_sent = example.select_one('.eg').text.strip()
                            examples.append(eg_sent)

                        if example.select_one('.trans'):
                            ch_sent = example.select_one('.trans').text.strip()
                            examples.append(ch_sent)




                    small_info = {'en_def':en_def, 'ch_def':ch_def, 'level':level, 'examples': examples, 'gcs': gcs}
                    big_sense['sense'].append(small_info)

                big_sense['extra_sents'] = extra_sents
                big_sense['guideword'] = guideword


                cam_dict[head_word][pos].append(big_sense)


# In[8]:


def start(url,head):

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    
    source_code = requests.get(url , headers=headers).content
    soup = BeautifulSoup(source_code, 'html.parser')
    extract(soup)


# In[28]:


if __name__ == '__main__':
    cam_dict = defaultdict(lambda:  defaultdict(lambda: []))    
    urls = eval(open('extendURLs.txt').read())
    for r in urls:
        print(r)
        w = r.split('/')[-1]
        if len(w.split('-')) < 2:
            start(r,r.split('/')[-1])
            
    import json
    with open('cambridge.word.json', 'w') as outfile:
        json.dump(cam_dict, outfile)


# In[6]:





# In[15]:





# In[ ]:




