from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import json
import io

import code

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
url = u'https://ask.helplib.com/t/数据结构'

def parse_answer(answer):
    content = answer.find('div', attrs={'class': 'qa-a-item-content'})
    content = content.find('div', attrs={'class': 'entry-content'})
    return ''.join([str(x) for x in content.contents])

def parse_question(href, m):
    print(href)
    r = requests.get(href, headers=headers)
    soup = BeautifulSoup(r.text)

    main = soup.find('div', attrs={'class': 'qa-q-view-main'})

    m['answer_list'] = []
    if not main:
        return m

    content = main.find('div', attrs={'class': 'qa-q-view-content'})
    content = content.find('div').find('div')
    content = ''.join([str(x) for x in content.contents])

    m['detail'] = content

    tags = soup.find('ul', attrs={'class': 'qa-q-view-tag-list'})
    tags = [x.text.strip() for x in tags.find_all('li', attrs={'class':'qa-q-item-tag-item'})]
    m['tags'] = tags

    answer_list = soup.find('div', attrs={'class': 'qa-a-list'})

    if not answer_list:
        return m

    #code.interact(local=locals())
    for answer in answer_list.find_all('div', attrs={'class': 'qa-a-list-item answer'}):
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

    items = soup.find_all('div', attrs={'class':'qa-q-item-title'})
    l = []
    for item in items:
        href = item.find('a').get('href')

        href = 'https://ask.helplib.com' + href
        if href in visited:
            continue
        m = {}
        m['title'] = item.find('a').text
        parse_question(href, m)

        visited[href] = True
        if not m['answer_list']:
            continue
        l.append(m)
    print()
    return l


if __name__ == '__main__':
    start = 320
    end = 1000
	
    l = []
    for page in range(start, end, 20):
        page_url = '%s/%d' % (url, page)
        l += parse_page(page_url)
    print(page)
    print(len(l))
    with io.open('output/helplib_数据结构_%d_%d.json' % (start, page), 'w', encoding='utf8') as f:
        f.write(json.dumps(l, ensure_ascii=False, indent=4))
    with io.open('output/visited.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(visited, ensure_ascii=False, indent=4))
