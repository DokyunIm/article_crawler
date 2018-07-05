import requests
import os
import time
import datetime
import json
from bs4 import BeautifulSoup
import get_joongang_detail as get_detail

try:
    req_url = "http://search.joins.com/TotalNews" # 요청 URL

    req_param = {
        'page': "1",
        "Keyword": "감자",
        "PeriodType": "DirectInput",
        #"StartSearchDate": "06/01/2018 00:00:00",
        #"EndSearchDate": "06/21/2018 00:00:00",
        "SortType": "New",
        "ScopeType": "All",
        "SourceGroupType": "Joongang",
        "SearchCategoryType": "TotalNews"
    }

    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'max-age=0'
    }

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 현재시간
    current_dir = os.getcwd() # 현재 디렉토리 경로
    if(os.path.isdir(current_dir+"/joongang") == False): # 폴더 생성
        os.makedirs(current_dir+"/joongang")

    fp_word_sentence_csv = open(current_dir+"/joongang/"+req_param['Keyword']+"_sentence_word("+str(now)+").csv", mode="w", encoding="utf-8") # 문장 단위 단어
    fp_word_article_csv = open(current_dir+"/joongang/"+req_param['Keyword']+"_article("+str(now)+").csv", mode="w", encoding="utf-8") # 기사 단위 단어
    fp_freq_word_json = open(current_dir+"/joongang/"+req_param['Keyword']+"_freq("+str(now)+").json", mode="w", encoding="utf-8") # 단어 빈도수
    fp_sentence_list_csv = open(current_dir+"/joongang/"+req_param['Keyword']+"_sentenct_list("+str(now)+").csv", mode="w", encoding="utf-8") # 문자 리스트

    idx = 0 # 기사 리스트 인덱스
    word_freq = dict() # 단어 빈도수

    while(idx<=50):
        idx += 1
        req_param['page'] = str(idx)
        req = requests.get(req_url, headers=req_headers, params=req_param)
        html = req.text
        header = req.headers
        status = req.status_code
        is_ok = req.ok
        soup = BeautifulSoup(html, 'html.parser')
        article_link_list = soup.select(".headline > a")

        if(len(article_link_list) == 0):
            break
        else:
            print("기사 수/페이지 : "+str(len(article_link_list)))
            for link in article_link_list:
                print(link['href'])

                word_article_list, word_sentence_list, word_list, sentence_list = get_detail.get(link['href'])

                if(len(word_article_list)>0):
                    fp_word_article_csv.write(word_article_list+"\n")

                if(len(word_sentence_list)>0):
                    for words in word_sentence_list:
                        fp_word_sentence_csv.write(words+"\n")

                if(len(word_list)>0):
                    for word in word_list:
                        if(word not in word_freq):
                            word_freq[word] = 1
                        else:
                            word_freq[word] += 1

                if(len(sentence_list)>0):
                    for sentence in sentence_list:
                        fp_sentence_list_csv.write(sentence+"\n")

                time.sleep(3.0)

    fp_freq_word_json.write(json.dumps(word_freq, ensure_ascii=False))

    fp_freq_word_json.close()
    fp_sentence_list_csv.close()
    fp_word_sentence_csv.close()
    fp_word_article_csv.close()

except:
    fp_freq_word_json.write(json.dumps(word_freq, ensure_ascii=False))

    fp_freq_word_json.close()
    fp_sentence_list_csv.close()
    fp_word_sentence_csv.close()
    fp_word_article_csv.close()
