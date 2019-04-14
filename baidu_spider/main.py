import io
import json

from bs4 import BeautifulSoup
import requests

from flask import Flask, request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
url = u'https://www.baidu.com/s?wd=%s'


def search_exactqa(wd):
    page_url = url % (wd)
    print(page_url)
    r = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(r.text)

    answers = soup.find_all('div', attrs={'class': 'op_exactqa_s_answer'})
    return [x.text for x in answers]


app = Flask(__name__)


@app.route("/search_exactqa")
def hello():
    wd = request.args.get('wd', '')
    return json.dumps(search_exactqa(wd), ensure_ascii=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
