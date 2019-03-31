import requests 
from bs4 import BeautifulSoup 
import operator 
from collections import Counter 
from collections import defaultdict
import re 
regex = re.compile(r'\[(.+?)\]')
brace_gx = re.compile(r'\((.+?)\)')
parts_map = {'U':'N','C':'N','S':'N', 'T':'V' ,'I':'V','L':'V','plural':'N','noun':'N','verb':'V','adjective':'ADJ'}
eng_set = set('a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(','))

def start_html(url,key):

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

    source_code = requests.get(url , headers=headers).text
    soup = BeautifulSoup(source_code, 'html.parser')

    tmp = []
    header = ""
    flag = False
    def_flag = False
    part = ""
    partsmap =""
    for each_text in soup.findAll('div', {'class':'entry-body__el clrd js-share-holder'}):
        semantic_tag = "NONE"
        for each in  each_text.findAll('div', {'class':'pos-header'}):
    #         print(' '.join(each.text.split('\n')[:2]).strip())
            header = ' '.join(each.text.split('\n')[:2]).strip()
            if len(each.text.split('\n'))>1:
                if each.text.split('\n')[1] in parts_map:
                    part = parts_map[each.text.split('\n')[1]]
                else:
                    part = each.text.split('\n')[1]
            else:
                if each.text.split(' ')[0] in parts_map:
                    if each.text.split(' ')[0] in parts_map:
                        part = parts_map[each.text.split(' ')[0]]
                    else:
                        part = each.text.split(' ')[0]
                else:
                    part = each.text.split(' ')[0]
            if regex.search(part):
                semantic_tag = regex.search(part).group(1).strip()
                indx = part.find(' [')
                part = part[:indx].strip()
                if part in parts_map:
                    part = parts_map[part]

        for each in each_text.findAll('div', {'class':'sense-block'}):
            for id,line in enumerate(each.text.split('\n')):
                line = line.strip()
                if 'More examples' in line or 'googletag.cmd' in line:
                    if len(tmp)>1:
                        if def_flag:
                            if not tmp[-1].split()[-1][0] in eng_set:
                                semanticDict[key]['def'][part][partsmap][semantic_tag].append(tmp)
                                def_flag = False
                        else:
                            if semanticDict[key]['ex']:
                                    semanticDict[key]['ex'].append(tmp)
                            else:
                                semanticDict[key]['ex'] = [tmp]
                        tmp = []
                    continue
                if flag:
                    if brace_gx.search(line):
                        semantic_tag = brace_gx.search(line).group(1).strip()
                    flag = False
                else:
                    if id == 0 and line == header:
                        if line and header:
                            flag = True
                    else:
                        if line:
                            line_split = line.split()[0]
#                             change here!!!
                            if line_split[0].isupper() and line_split[-1].isdigit() or line[0]=='›' :
                                tmp.append(line)
                                if regex.search(line[2:]):
                                    partsmap = regex.search(line[2:]).group(1).strip()
                                else:
                                    partsmap = "NONE"
                                def_flag = True
                            else:
#                                 print(id,line)
                                tmp.append(line)
                                if len(tmp)==2:
                                    if line.split()[-1][-1].lower() in eng_set:
                                        if any([r in tmp for r in ['Opposite','Synonym','See also','Compare','See']]):
                                            tmp = []
                                        continue

                                    if def_flag:
                                        semanticDict[key]['def'][part][partsmap][semantic_tag].append(tmp)
                                        def_flag = False
                                    else:
                                        if semanticDict[key]['ex']:
                                            semanticDict[key]['ex'].append(tmp)
                                        else:
                                            semanticDict[key]['ex'] = [tmp]
                                    tmp = []
                                elif len(tmp)==3:
                                    if def_flag:
                                        if regex.search(tmp[0]) and tmp[0][:len(key)] == key:
                                            partsmap = regex.search(tmp[0]).group(1).strip()
                                        semanticDict[key]['def'][part][partsmap][semantic_tag].append(tmp)
                                        def_flag = False
                                    else:
                                        if semanticDict[key]['ex']:
                                                semanticDict[key]['ex'].append(tmp)
                                        else:
                                            semanticDict[key]['ex'] = [tmp]
                                    tmp = []
                                elif len(tmp)>3:
                                    print(tmp)
                                    if tmp[-1].split()[-1][-1].lower() in eng_set:
                                        continue
                                    else:
                                        if def_flag:
                                            if regex.search(tmp[0]) and tmp[0][:len(key)] == key:
                                                partsmap = regex.search(tmp[0]).group(1).strip()
                                            semanticDict[key]['def'][part][partsmap][semantic_tag].append(tmp)
                                            def_flag = False
                                        else:
                                            if semanticDict[key]['ex']:
                                                    semanticDict[key]['ex'].append(tmp)
                                            else:
                                                semanticDict[key]['ex'] = [tmp]
                                        tmp = []

            if  def_flag and tmp:
                semanticDict[key]['def'][part][partsmap][semantic_tag].append(tmp)
                def_flag = False
            elif tmp:
                if semanticDict[key]['ex']:
                        semanticDict[key]['ex'].append(tmp)
                else:
                    semanticDict[key]['ex'] = [tmp]
                tmp = []

semanticDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list)))))

if __name__ == '__main__':
    urls = eval(open('extendURLs.txt').read())

    for r in urls[:10]:
        start_html(r,r.split('/')[-1])
        
    import json
    with open('cambridge.dictionary.json','w') as fd:
        json.dump(semanticDict,fd)
