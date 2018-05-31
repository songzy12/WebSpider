#encoding=utf8

from bs4 import BeautifulSoup
import requests
import code
from collections import defaultdict
import json
import io

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

def find_topic_by_keyword(keyword):
    url = 'https://www.zhihu.com/search?type=topic&q=' + keyword
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text)

    href = soup.find('a', attrs={'class':'name-link'}).get('href')
    return href[len('/topic/'):]

def find_links_by_topic(topic):
    url = 'https://www.zhihu.com/topic/'+topic+'/top-answers'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text)

    num_page = soup.find('div', attrs={'class':'zm-invite-pager'}).find_all('span')[-2].text 
    num_page = int(num_page)
    print 'num_page:', num_page

    links = []

    for i in range(1, num_page+1):
        page_url = url + '?page=' + str(i)
        print page_url

        r = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(r.text)

        for content in soup.find_all('div', attrs={'data-type':'Answer'}):
            links.append(content.link.get('href'))

    return links

def get_qa_by_topic_link(link):
    url = 'https://www.zhihu.com' + link
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text)

    title = soup.find('h1', attrs={'class':'QuestionHeader-title'}).text
    detail = soup.find('div', attrs={'class': 'QuestionHeader-detail'}).text
    keywords = soup.find('meta', attrs={'itemprop':'keywords'}).get('content')
    vote = soup.find('button', attrs={'class': 'Button VoteButton VoteButton--up'}).text

    print title 

    answer = soup.find('div', attrs={'class':'RichContent-inner'}).text

    return {'title': title, 'detail': detail, 'keywords': keywords.split(','), 'answer': answer, 'link': link, 'vote': vote} 


def get_qa_by_keywords(keywords):
    for keyword in keywords:
        topic = find_topic_by_keyword(keyword)
        print 'topic id: ', topic
        
        links = find_links_by_topic(topic)
        print 'num_link:', len(links)
        m = [] 
        for link in links:
            qa = get_qa_by_topic_link(link)
            m.append(qa)

        path = 'data/zhihu'+'-'+topic+'.json'
        with io.open(path, 'w', encoding='utf8') as f:
            f.write(json.dumps(m, ensure_ascii=False, indent=4))

if __name__ == '__main__':
    keywords = [u'认知心理学', u'社会心理学', u'认知神经科学', u'消费心理学', u'人格']
    get_qa_by_keywords(keywords)
