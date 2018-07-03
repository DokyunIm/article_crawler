import requests
import os
from bs4 import BeautifulSoup
import time
import json
import get_chosun_detail as get_detail


#get_detail.get("http://news.chosun.com/site/data/html_dir/2018/01/23/2018012300267.html")


req_url = "http://search.chosun.com/search/news.search"

req_param = {
    "query": "감자",
    "pageno": "0",
    "orderby": "news",
    "categoryname": "조선일보",
    "c_scope": "navi",
    "sdate": "2018.01.01",
    "edate": "2018.06.25"
}

req_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

current_dir = os.getcwd()
if(os.path.isdir(current_dir+"/chosun") == False):
    os.makedirs(current_dir+"/chosun")

fp_result_sentence_csv = open(current_dir+"/chosun/"+req_param['query']+"_sentence.csv", mode="w", encoding="utf-8")
fp_result_article_csv = open(current_dir+"/chosun/"+req_param['query']+"_article.csv", mode="w", encoding="utf-8")
fp_result_freq_word_txt = open(current_dir+"/chosun/"+req_param['query']+"_freq.csv", mode="w", encoding="utf-8")
result_word_list = dict()
idx = 0

while(idx<=25):
    idx += 1
    req_param['pageno'] = str(idx)
    req = requests.get(req_url, headers=req_headers, params=req_param)
    html = req.text
    header = req.headers
    status = req.status_code
    is_ok = req.ok
    soup = BeautifulSoup(html, 'html.parser')
    #article_link_list = soup.findAll("strong", {"class": "headline mg"})
    article_link_list = soup.select(".search_news_box > dl > dt > a")
    #body > div.schCont > div > div.l_area > div.search_news_box > dl: nth - child(2) > dt > a
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

fp_result_freq_word_txt.write(json.dumps(result_word_list, ensure_ascii=False))

fp_result_sentence_csv.close()
fp_result_article_csv.close()
fp_result_freq_word_txt.close()
