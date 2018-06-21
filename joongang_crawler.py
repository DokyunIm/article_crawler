import requests
import json
from bs4 import BeautifulSoup
import get_joongang_detail as get_detail
import operator


req_url = "http://search.joins.com/TotalNews"

req_param = {
    'page': "1",
    "Keyword": '감자',
    "PeriodType": "DirectInput",
    #"StartSearchDate": "06/01/2018 00:00:00",
    #"EndSearchDate": "06/21/2018 00:00:00",
    "SortType": "New",
    "ScopeType": "Title",
    "SourceGroupType": "Joongang",
    "SearchCategoryType": "TotalNews"
}

req_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

"""
req = requests.get(req_url, headers=req_headers, params=req_param)
html = req.text
header = req.headers
status = req.status_code
is_ok = req.ok
soup = BeautifulSoup(html, 'html.parser')
#article_link_list = soup.findAll("strong", {"class": "headline mg"})
article_link_list = soup.select(".headline > a")
get_detail.get(article_link_list[0]['href'])
"""
word_list = dict()
idx = 0
while(idx<=5):
    idx += 1
    req_param['page'] = str(idx)
    req = requests.get(req_url, headers=req_headers, params=req_param)
    html = req.text
    header = req.headers
    status = req.status_code
    is_ok = req.ok
    soup = BeautifulSoup(html, 'html.parser')
    #article_link_list = soup.findAll("strong", {"class": "headline mg"})
    article_link_list = soup.select(".headline > a")
    if(len(article_link_list) == 0):
        break;
    else:
        print(len(article_link_list))
        for link in article_link_list:
            print(link['href'])
            article_word_list = get_detail.get(link['href'])
            for word in article_word_list:
                if(word not in word_list):
                    word_list[word] = 1
                else:
                    word_list[word] += 1

sorted_word_list = sorted(word_list.items(), key=operator.itemgetter(1), reverse=True)

fp = open(req_param['Keyword'], "w")
fp.write(str(word_list))

fp_sorted = open("sorted_"+req_param['Keyword'], "w")
fp_sorted.write(str(sorted_word_list))

print(word_list)
print(sorted_word_list)
fp.close()
fp_sorted.close()



