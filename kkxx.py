import requests

def get_content(page_number):

    url = 'http://zhjw.cic.tsinghua.edu.cn/xkYjs.vxkYjsJxjhBs.do'
    headers = {'Host': 'zhjw.cic.tsinghua.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://zhjw.cic.tsinghua.edu.cn/xkYjs.vxkYjsJxjhBs.do',
    'Cookie': 'LRy_qkey=LRKPZYyU7XI5LJIH1NZBvVP4e39mpw46; JSESSIONIDJXPGNEW=abcWytI85uie89iK8XEGv; thuwebcookie=1778675466.20480.0000; JSESSIONID=abc215YdTdP4x-CC8XEGv',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'}
    payload = dict(m='kkxxSearch',
                   page=page_number,
                   token='dd052dee77afe69f0c2aa3643ea47ffa',
                   p_sort = {'asc1': 'true', 'asc2':'true'},
                   p_xnxq='2016-2017-1',
                   pathContent='%E5%BC%3F%AF%BE%E4%BF%A1%E6%81%AF%E6%9F%A5%E8%AF%A2',
                   goPageNumber=2)
    r = requests.post(url, data=payload, headers=headers)
    return r.content

print get_content(5)