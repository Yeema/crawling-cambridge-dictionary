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

semanticDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list)))))

def start(url,head):

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    
    source_code = requests.get(url , headers=headers).text 
    soup = BeautifulSoup(source_code, 'html.parser') 

    # Text in given web-page is stored under 
    # the <div> tags with class <entry-content> 
    for each_text in soup.findAll('div', {'class':'sense-block'}): 
        clean_sent(each_text.text,head)
        
semanticDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list)))))
def build_dict(head,string,skip = 0,semantic_tag = "NONE",definition = "NONE",output_part = "NONE"):
    special = False
    example = []
    output_part = ""
    part_str = "NONE"
    ex_id = 0
    print('------->', head)
#     print(string)
    for idx , s in enumerate(string):
        cond = s.split()[0]

        if semantic_tag != "NONE" and skip > 0 and definition == "NONE":
            skip -= 1
            continue

        if skip>0:
            definition.append(s)
            ex_id = idx+1
            if output_part:
                semanticDict[head]['def'][semantic_tag][output_part][part_str].append(definition)
            else:
                semanticDict[head]['def'][semantic_tag]['NONE'][part_str].append(definition)
            skip -= 1
            print('^^^^^', output_part, '||', semantic_tag, '||', part_str)
            continue
            
        if cond == head and idx+1 < len(string):
            special = True
            print(s)
            if s.split()[1].strip() in parts_map:
                output_part = parts_map[s.split()[1].strip()]
            elif not output_part:
                output_part = "NONE"
            if regex.search(s):
                part_str = regex.search(s).group(1).strip()
            else:
                part_str = "NONE"
            if brace_gx.search(string[idx+1]):
                semantic_tag = brace_gx.search(string[idx+1]).group(1).strip()
                skip = 1
            else:
                semantic_tag = s
            continue
        if brace_gx.search(s):  
            print(semantic_tag)
            semantic_tag = brace_gx.search(s).group(1).strip()    
            if semantic_tag.split()[0].isupper():
                continue
                
        if cond[0].isupper() and cond[-1].isdigit() or '›' == cond[0]:
            if regex.search(s):
                part_str = regex.search(s).group(1).strip()
                parts = part_str.split('or')
                for part in parts:
                    part = part.strip().split(' ')[0]
                    if part in parts_map:
                        output_part = parts_map[part]
                        break
                    else:
                        output_part = part
#                 s_id = max(s.find(']'),s.find('>'))
                definition = [s.strip()]
            else:
                definition = [s.strip()]
            skip = 1
            print('def:', definition)
        else:
            if idx == 0:
                semantic_tag = s
                print(s)
            else:
                if (idx-ex_id)%2==0:
                    if s.split()[-1][0].lower() in eng_set:
                        example = [s]
                else:
                    if len(example)==1:
                        example.append(s)
                        if semanticDict[head]['example']:
                            semanticDict[head]['example'].append(example)
                        else:
                            semanticDict[head]['example'] = []
                            semanticDict[head]['example'].append(example)
                            #semanticDict[head][]
                print(example)
                
    return semanticDict

def clean_sent(sents,head):
    string = []
    example = []
#     for sent in sent_tokenize(sents.strip()):
    for sent in sents.strip().split('\n'):
        for s in sent.split('\n'):
            s = s.strip()
            if s:
                if '更多範例' == s[:4] :
                    return build_dict(head,string)
                else:
                    string.append(s)
    return build_dict(head,string)

if __name__ == '__main__':
    urls = eval(open('extendURLs.txt').read())
    for r in urls[:1]:
        print(r)
        start(r,r.split('/')[-1])
        
    import json
    #for line in semanticDict.items():
    #    print(line)
    #print(semanticDict)
    #with open('cambridge.dictionary.json','w') as fd:
        #json.dump(semanticDict,fd)