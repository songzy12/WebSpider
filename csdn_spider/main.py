from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import json
import io

import code

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
url = u'http://ask.csdn.net/questions/tags/search?id=数据结构'

def parse_answer(answer):
    return ''.join([str(x) for x in answer.find('div').contents])

def parse_question(href):
    print(href)
    r = requests.get(href, headers=headers)
    soup = BeautifulSoup(r.text)
    
    m = {}
    
    detail = soup.find('div', attrs={'class': 'questions_detail_con'})
    dl = detail.find('dl')
    question = dl.find('dt').text.strip()
    m['title'] = question
    m['detail'] = str(dl.find('dd'))

    tags = detail.find('div', attrs={'class': 'tags'})
    tags = [x.text for x in tags.findChildren()]
    m['tags'] = tags
    
    answer_list = soup.find('div', attrs={'class': 'answer_list'})
    m['answer_list'] = []

    if not answer_list:
        return m

    #code.interact(local=locals())
    for answer in answer_list.find_all('div', attrs={'class': 'answer_accept'}):
        m['answer_list'].append(parse_answer(answer))
        
    for answer in answer_list.find_all('div', attrs={'class': 'answer_detail_con'}):
        m['answer_list'].append(parse_answer(answer))
    return m
        
try:
    with open('output/visited.json') as f:
        visited = json.loads(f.read())
except:
    visited = {}

print("len(visited):", len(visited))

def parse_page(page_url):
    print(page_url)
    r = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(r.text)
    dts = soup.find_all('dt')
    l = []
    for dt in dts:
        href = dt.find('a').get('href')
        if href in visited:
            continue
            
        m = parse_question(href)
        visited[href] = True
        if not m['answer_list']:
            continue
        l.append(m)
    return l

if __name__ == '__main__':
    l = []
    start = 0
    end = 88 
    try:      
        for page in range(start, end):
            page_url = '%s&page=%d' % (url, page+1)
            l += parse_page(page_url)
    except:
        print(page)
    print(len(l))
    with io.open('output/csdn_数据结构_%d_%d.json' % (start, page), 'w', encoding='utf8') as f:
        f.write(json.dumps(l, ensure_ascii=False, indent=4))
    with io.open('output/visited.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(visited, ensure_ascii=False, indent=4))
