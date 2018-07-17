# encoding=utf8

from bs4 import BeautifulSoup
import requests
import code
from collections import defaultdict
import json
import io

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

# href = soup.find('a', attrs={'class':'name-link'}).get('href')
# num_page = soup.find('div', attrs={'class':'zm-invite-pager'}).find_all('span')[-2].text
# for content in soup.find_all('div', attrs={'data-type':'Answer'}):
# links.append(content.link.get('href'))
# title = soup.find('h1', ).text
# detail = soup.find('div', attrs={'class': 'QuestionHeader-detail'}).text
# keywords = soup.find('meta', attrs={'itemprop':'keywords'}).get('content')
# vote = soup.find('button', attrs={'class': 'Button VoteButton VoteButton--up'}).text
# answer = soup.find('div', attrs={'class':'RichContent-inner'}).text

URL = 'https://www.diyidan.com/main/post/6294360860138371261/detail/'
N_PAGE = 52

user2audio = [] 
url_set = set()


def parse_page(page):
    url = "%s%d" % (URL, page)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text)
    for reply_right in soup.find_all('div', attrs={'class': 'reply_right'}):
        user_name_span = reply_right.find(
            'div', attrs={'class': 'user_name'}).find('span')
        user_name = user_name_span.text
        user_page = user_name_span.get('onclick').split('\'')[1]

        try:
            audio_src = reply_right.find('audio').get('src')
        except:
            continue
        print("%s\t%s" % (user_name, audio_src))
        if audio_src not in url_set:
            url_set.add(audio_src)
            user2audio.append(
                {'user_name': user_name, 'user_page': 'www.diyidan.com' + user_page, 'audio_src': audio_src[2:]})


if __name__ == '__main__':
    for page in range(1, N_PAGE + 1):
        print("page %d" % page)
        parse_page(page)
    with io.open('data/user2audio.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(user2audio, ensure_ascii=False, indent=4))
