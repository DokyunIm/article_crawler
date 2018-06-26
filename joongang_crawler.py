import requests
import os
import time
from bs4 import BeautifulSoup
import get_joongang_detail as get_detail


req_url = "http://search.joins.com/TotalNews"

req_param = {
    'page': "1",
    "Keyword": "감자",
    "PeriodType": "DirectInput",
    #"StartSearchDate": "06/01/2018 00:00:00",
    #"EndSearchDate": "06/21/2018 00:00:00",
    "SortType": "New",
    "ScopeType": "Title",
    "SourceGroupType": "Joongang",
    "SearchCategoryType": "TotalNews"
}

req_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0'
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
current_dir = os.getcwd()
if(os.path.isdir(current_dir+"/joongang") == False):
    os.makedirs(current_dir+"/joongang")

fp_result_sentence_csv = open(current_dir+"/joongang/"+req_param['Keyword']+"_sentence.csv", mode="w", encoding="utf-8")
fp_result_article_csv = open(current_dir+"/joongang/"+req_param['Keyword']+"_article.csv", mode="w", encoding="utf-8")
fp_result_freq_word_txt = open(current_dir+"/joongang/"+req_param['Keyword']+"_freq.txt", mode="w", encoding="utf-8")
result_word_list = dict()
idx = 0

while(idx<=20):
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
        break
    else:
        print(len(article_link_list))
        for link in article_link_list:
            print(link['href'])
            article_list, sentence_list, word_list = get_detail.get(link['href'])
            for word in word_list:
                if (word not in result_word_list):
                    result_word_list[word] = 1
                else:
                    result_word_list[word] += 1
            if(len(article_list) > 0):
                fp_result_article_csv.write(article_list+"\n")
                for sentence in sentence_list:
                    if(len(sentence)!=0):
                        fp_result_sentence_csv.write(sentence+"\n")
            time.sleep(3.0)

fp_result_freq_word_txt.write(str(result_word_list))

fp_result_sentence_csv.close()
fp_result_article_csv.close()
fp_result_freq_word_txt.close()












"""
for word in article_word_list:
    if(word not in word_list):
        word_list[word] = 1
    else:
        word_list[word] += 1
"""

"""
sorted_word_list = sorted(word_list.items(), key=operator.itemgetter(1), reverse=True)

fp = open(req_param['Keyword'], "w")
fp.write(str(word_list))

fp_sorted = open("sorted_"+req_param['Keyword'], "w")
fp_sorted.write(str(sorted_word_list))

print(word_list)
print(sorted_word_list)
fp.close()
fp_sorted.close()
"""


