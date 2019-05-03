import io
import json
from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}


def search_exactqa(wd):
    url = u'https://www.baidu.com/s?wd=%s'
    page_url = url % (wd)
    # print(page_url)
    r = requests.get(page_url, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text)

    answers = soup.find_all('div', attrs={'class': 'op_exactqa_s_answer'})
    return [x.text for x in answers]


def search_zhidao(wd):
    url = "https://zhidao.baidu.com/search?word=%s"
    page_url = url % wd
    print(page_url)

    r = requests.get(page_url, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text)

    def get_page_num(soup):
        pager = soup.find('div', attrs={'class': 'pager'})
        pager_last = pager.find('a', attrs={'class': 'pager-last'})
        href = pager_last.get('href')
        return int(href.split("=")[-1])

    def search_page_num(wd, page_num):
        # TODO
        url = "https://zhidao.baidu.com/search?word=%s&pn=%d"
        page_url = url % (wd, page_num)
        print(page_url)

        r = requests.get(page_url, headers=headers)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text)
        dls = soup.find_all('dl')

        res = []
        for dl in dls:
            ti = dl.find('a', attrs={'class': 'ti'})
            question_url = ti.get('href')
            agree = dl.find('span', attrs={'class': 'f-black'})
            agree = int(agree.text.strip())
            res.append([question_url, agree])

        return res

    def search_question_url(question_url):
        print(question_url)
        r = requests.get(question_url, headers=headers)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text)

        question = soup.find('span', attrs={'class': 'ask-title'})

        answer = soup.find('div', attrs={'class': 'wgt-best'})
        answer = answer.find('div', attrs={'class': 'best-text'})

        return question.text.strip(), answer.text.strip()

    max_page_num = get_page_num(soup)
    res = []
    for page_num in range(0, max_page_num + 1, 10):
        question_urls = search_page_num(wd, page_num)
        for question_url, agree in question_urls:
            try:
                question, answer = search_question_url(question_url)
            except:
                # when there is not wge-best
                continue
            res.append({
                "question_url": question_url,
                "question": question,
                "answer": answer,
                "agree": agree
            })
    res.sort(key=lambda x: -x['agree'])
    return res


if __name__ == '__main__':
    wd = "二叉查找树"
    m = {}
    m[wd] = search_zhidao(wd)
    with io.open('baidu_zhidao.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(m, ensure_ascii=False, indent=4))
