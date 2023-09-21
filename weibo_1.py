# 爬取微博话题主页内容
# 对于不同的微博话题，更改项：page/url/Cookie

import csv
import requests
from bs4 import BeautifulSoup

def reptile_synthesize(headers):
    global url
    page = 1
    data_list = []

    while page <= 18:
        url_new = url + str(page)
        res = requests.get(url_new, headers=headers)
        res.encoding = 'utf-8'
        bs = BeautifulSoup(res.text, 'html.parser')
        comment = bs.find_all('div', class_='card-feed')
        for content in comment:
            data = content.find('div', class_='content').find('p', class_='txt').text
            print(data)
            data_info = {'评论': data}
            data_list.append(data_info)
        page += 1

    with open('./data/comment_1.csv', 'a', encoding='gb18030', newline='') as f:
            comment_csv = csv.DictWriter(f, fieldnames=['评论'])
            comment_csv.writeheader()
            comment_csv.writerows(data_list)



if __name__ == '__main__':
    url = 'https://s.weibo.com/weibo?q=%23%E8%85%BE%E8%AE%AF%E8%A7%86%E9%A2%91%E6%AC%BA%E9%AA%97%E6%B6%88%E8%B4%B9%E8%80%85%23&page='

    reptile_synthesize(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
                'Cookie': 'SINAGLOBAL=4620999836278.491.1635497490356; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWh'
                          'q-DgG04vhTgrgvhR85ZC5JpX5KzhUgL.FoMfeKqRShe0eK52dJLoIf2LxKnL1h5L1heLxKMLBK5L1KBLxKBLB'
                          '.2LB.2LxKMLB.-L12-LxK-LBK-LB.BLxKML1-2L1hBLxK-L12qL1hnLxKBLBonL1h5LxK-LBKBLBK.t; UOR=p'
                          'assport.weibo.com,weibo.com,login.sina.com.cn; ULV=1678271041384:5:5:5:2732818897478.5'
                          '57.1678271041326:1678256378081; ALF=1709806967; PC_TOKEN=e40681fbfb; SUB=_2A25JDBGoDeR'
                          'hGeFL6lQZ9C3PyjyIHXVqeARgrDV8PUNbmtAGLWz5kW9NQn0WUVoMHDMpb8LNyFnWuuZmlH95pqpk; SSOLogi'
                          'nState=1678270968; _s_tentry=weibo.com; Apache=2732818897478.557.1678271041326'
            })

    print('爬取完成！')

