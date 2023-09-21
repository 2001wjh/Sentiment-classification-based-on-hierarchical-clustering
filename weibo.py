# 爬取微博话题详情页内容
# 对于不同的微博话题详情页，更改项：url/url_next/Cookie
import requests
import random
import time
import csv


def get_maxid(url, headers):
    requests.packages.urllib3.disable_warnings()
    time.sleep(0.5)
    response = requests.get(url, headers=headers, verify=False)
    data_json = response.json()
    return data_json['max_id']

def get_comment(url, headers):
    global Comment_list
    requests.packages.urllib3.disable_warnings()
    time.sleep(0.5)
    response = requests.get(url, headers=headers, verify=False)
    data_json = response.json()
    data_list = data_json['data']
    for data in data_list:
        print(data['text_raw'])
        data_info = {'评论': data['text_raw']}
        Comment_list.append(data_info)

def save_comment(data_list):
    with open('./data/comment.csv', 'a', encoding='gb18030', newline='') as f:
            comment_csv = csv.DictWriter(f, fieldnames=['评论'])
            comment_csv.writerows(data_list)

def get_url(maxid):
    url_next = 'https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id=4526958438619943&is_sho' \
               'w_bulletin=2&is_mix=0&max_id={}&count=20&uid=1642634100'.format(maxid)
    return url_next

if __name__ == '__main__':
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]

    headers = {
        'Connection': 'close',
        'Cookie': 'SINAGLOBAL=4620999836278.491.1635497490356; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWhq-DgG04vhTgrgvhR85ZC5JpX5K'
                  'zhUgL.FoMfeKqRShe0eK52dJLoIf2LxKnL1h5L1heLxKMLBK5L1KBLxKBLB.2LB.2LxKMLB.-L12-LxK-LBK-LB.BLxKML1-2L1hBLxK-L12qL1h'
                  'nLxKBLBonL1h5LxK-LBKBLBK.t; UOR=passport.weibo.com,weibo.com,login.sina.com.cn; ULV=1678784383500:8:8:2:62456318'
                  '69704.086.1678784383313:1678701751154; ALF=1710320317; WBPSESS=RvB-1g6yfMuxfMw3NjqmMR3HGNQejXji1wOKe8SWxRyNCCIoo'
                  'bJxG0L-SgMis_DQPK6vfjfr-26N4QPtOhvaG9gU-KEwVt1lr03Le6N_yQQM-lJDKa9ulpK3c0UDmIdo9lBN6umYCx2_k2YK5RHEfg==; PC_TOKE'
                  'N=a68b48accf; SUB=_2A25JFEdvDeRhGeFL6lQZ9C3PyjyIHXVqYD-nrDV8PUNbmtANLRCjkW9NQn0WURE1cNatFGsYb0Zpnc3MUyibmvR0; SS'
                  'OLoginState=1678784319; XSRF-TOKEN=UZ7wpSgK1Bxm13-5xW5nUYqJ; _s_tentry=weibo.com; Apache=6245631869704.086.167878'
                  '4383313',
        'User-Agent': ''
               }
    headers['User-Agent'] = random.choice(user_agent_list)
    url = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4526958438619943&is_show_bulletin=2&is_mix=0&count=10&uid=1642634100'
    Comment_list = []
    order = 0

    while order <= 150:
        order += 1

        get_comment(url, headers)
        max_id = get_maxid(url, headers)
        url = get_url(max_id)

    save_comment(Comment_list)
    print('爬取完成！')




