#encoding=utf8

from bs4 import BeautifulSoup
import code
from collections import defaultdict
import cookielib
import io
import json
import requests

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8,ja-JP;q=0.6,ja;q=0.4,en;q=0.2',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'d_c0="AFCCx_neAgyPTk8QDI5BAciPPot27zRNYHU=|1499131099"; _zap=1ca51403-2f21-4abe-946f-1d3388171015; q_c1=9560bd1483854135adc702c93722e953|1504499173000|1499131099000; aliyungf_tc=AQAAAEpOVi+/fAMABfQGZR2vBf7CJ2fM; s-q=%E5%BF%83%E7%90%86%E5%AD%A6; s-i=1; sid=vnlaj0ag; r_cap_id="MjlhZThmM2VmNWZkNGY1Y2JhYTE1ZGEzMzhkNzc4OWU=|1505129840|b8173a4a32a7ee0175641825a259c8e495adc495"; cap_id="OWY3NjY0ZjQwODZkNDNmNzhjNWUwYjVhZjE1MjQyYjI=|1505129840|2a410239ede9e87c808970f88ad7b87d001076a0"; __utma=51854390.1485811755.1499131100.1505121836.1505128843.8; __utmb=51854390.0.10.1505128843; __utmc=51854390; __utmz=51854390.1505128843.8.5.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.000--|2=registration_date=20140921=1^3=entry_date=20170704=1; z_c0=Mi4xanR4OUFBQUFBQUFBVUlMSC1kNENEQmNBQUFCaEFsVk5kd0xlV1FBcFBmMUVsZHF2R29leXVOMEFONUNCYWs2YXdn|1505129847|ead7b4b3cd0aba416db33bba8d49f3b506398f2d; _xsrf=a164d0f5-8910-4bca-99a8-1578cff67df6',
'Host':'www.zhihu.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
}

def login():
    username = raw_input('phone_num: ')
    password = raw_input('password: ')
    cap_url = 'https://www.zhihu.com/captcha.gif?r=1466595391805&type=login'
    cap_content = session.get(cap_url, headers=headers).content
    cap_file = open('./cap.gif', 'wb')
    cap_file.write(cap_content)
    cap_file.close()    
    captcha = raw_input('captcha: ')
    url = 'https://www.zhihu.com/login/phone_num'
    
    post_data = {'phone_num': username, 'password': password, 'captcha': captcha}
    login_page = session.post(url, data=post_data, headers=headers)
    login_code = eval(login_page.text)
    print login_code['msg']
    session.cookies.save()

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print 'Cookie load failed'
    login()

'''
def get_links_by_people_topic(people, topic):
    url = 'https://www.zhihu.com/people/' + people + '/answers/topic/' + topic
    print url
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text)
    
    try:
        num_page = soup.find('div', attrs={'class':'Pagination'}).find_all('button')[-2].text 
        num_page = int(num_page)
    except:
        num_page = 1
    print 'num_page:', num_page

    links = []
    
    
    for i in range(1, num_page+1):
        page_url = url + '?page=' + str(i)
        print page_url

        r = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(r.text)

        print soup.prettify()
        
        local = locals()
        local.update(globals())
        code.interact(local=local)

        for content in soup.find_all('a', attrs={'data-za-detail-view-element_name':'Title'}):
            links.append(content.get('href'))
    print 'num_links:', len(links)
    return links
'''

def get_qa_by_link(link):
    url = 'https://www.zhihu.com' + link
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text)
    try:
        title = soup.find('h1', attrs={'class':'QuestionHeader-title'}).text
        detail = soup.find('div', attrs={'class': 'QuestionHeader-detail'}).text
        keywords = soup.find('meta', attrs={'itemprop':'keywords'}).get('content')
        vote = soup.find('button', attrs={'class': 'Button VoteButton VoteButton--up'}).text

        print title 

        answer = soup.find('div', attrs={'class':'RichContent-inner'}).text
    except:
        code.interact(local=locals())
    return {'title': title, 'detail': detail, 'keywords': keywords.split(','), 'answer': answer, 'link': link, 'vote': vote} 

def find_topic_by_keyword(keyword):
    url = 'https://www.zhihu.com/search?type=topic&q=' + keyword
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text)

    href = soup.find('a', attrs={'class':'name-link'}).get('href')
    return href[len('/topic/'):]

def get_writers_by_topic(topic):
    url = 'https://www.zhihu.com/topic/'+topic+'/top-writer'
    print url
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text)
    icons = soup.find_all('span', attrs={'class': 'icon icon-badge-id-an icon-badge'})
    writers = []
    for icon in icons:
        writer = icon.previous_sibling
        print writer.get('href'), writer.text
        writers.append(writer.get('href')[len('/people/'):])
    if not writers:
        print soup.prettify()
        code.interact(local=locals())
    return writers

def get_qas_by_people_topic(people, topic):
    qas = []
    offset = 0
       
    
    try:
        while True:
            url = 'https://www.zhihu.com/api/v4/members/'+people+'/topics/'+topic+'/answers?data%5B%2A%5D.author.badge%5B%3F%28type=best_answerer%29%5D.topics&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees&limit=20&offset='+str(offset)+'&sort_by=created'
            content = session.get(url, headers=headers).text
            r = json.loads(content)
            
            print people, offset
            
            for item in r['data']:
                content = item['content']
                title = item['question']['title']
                voteup_count = item['voteup_count']
                qas.append({'title': title, 
                            'content': content, 
                            'voteup_count': voteup_count})

            if r['paging']['is_end']:
                break
            offset += 20
            
    except:
        print url
        print r['error']['message']
        local = locals()
        local.update(globals())        
        code.interact(local=locals())
    return qas    

if __name__ == '__main__':
    keywords = [u'认知神经科学', u'心理学', u'认知心理学', u'社会心理学', u'消费心理学', u'人格']
    keyword = keywords[0]
    topic = find_topic_by_keyword(keyword)
    print 'topic id:', topic
    writers = get_writers_by_topic(topic)

    path = 'data/zhihu-topic-'+topic+'-top-writers.json'
    with io.open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(writers, ensure_ascii=False, indent=4))      
        
    for writer in writers:
        temp = get_qas_by_people_topic(writer, topic)
        path = 'data/zhihu-people-'+writer+'-topic-'+topic+'.json'
        print path
        with io.open(path, 'w', encoding='utf8') as f:
            f.write(json.dumps(temp, ensure_ascii=False, indent=4))      
        


'''
        links = get_links_by_people_topic(writer, topic)
        qas = []
        for link in links:
            qa = get_qa_by_link(link)
            qas.append(qa)
        path = 'data/zhihu-people-'+writer+'-topic-'+topic+'.json'
        with io.open(path, 'w', encoding='utf8') as f:
            f.write(json.dumps(qas, ensure_ascii=False, indent=4))            
'''
