import json
import os
import requests
import time
import datetime
from bs4 import BeautifulSoup
import operator
import get_kyunghyang_detail as get_detail
from collections import defaultdict

#container > div.content > div.news.section > dl:nth-child(2) > dt > a
#container > div.content > div.news.section > dl:nth-child(2) > dt > a

# Request Param Setting
# Request Param Setting
req_url = "http://search.khan.co.kr/search.html"
req_header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.' }
req_param = {
    "pg" : "1",
    "q" : "토마토",
    "d1" : "20180301~20180626", # 시작일~종료일
    "Sort" : "1",  # 1: 최신순 2: 정확도순 3: 오래된순
    "stb": "khan", # 경향신문만 검색
}

now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')  # 현재시간
current_dir = os.getcwd()  # 현재 디렉토리 경로
if (os.path.isdir(current_dir + "\kyunghyang") == False):  # 폴더 생성
    os.makedirs(current_dir + "\kyunghyang")

f = open("./kyunghyang/" + 'freq_output.csv', 'w')
fp_word_sentence_csv = open("./kyunghyang/" + req_param['q'] + "_sentence_word(" + str(now) + ").csv", mode="w", encoding="utf-8")  # 문장 단위 단어
fp_word_article_csv = open("./kyunghyang/" + req_param['q'] + "_article(" + str(now) + ").csv", mode="w", encoding="utf-8")  # 기사 단위 단어
# fp_freq_word_json = open(current_dir + "/kyunghyang/" + req_param['Keyword'] + "_freq(" + str(now) + ").json", mode="w", encoding="utf-8")  # 단어 빈도수
fp_sentence_list_csv = open("./kyunghyang/" + req_param['q'] + "_sentenct_list(" + str(now) + ").csv", mode="w", encoding="utf-8")  # 문자 리스트

# Request sequentially until page end and Extract Article Link from Response
idx = 0
article_link = { "amount" : 0, "links" : [] }
# words = ""
# words = [] # 리스트로 반환시켜보자
word_freq = defaultdict(int) # 정수를 값으로 갖는 dictionary

while(1):
    idx += 1
    req_param['pg'] = str(idx)
    res = requests.get(req_url, headers=req_header, params=req_param)
    res_text = res.text

    res_soup = BeautifulSoup(res_text, 'html.parser')
    res_soup_headlines = res_soup.select('.phArtc > dt > a')
    if len(res_soup_headlines) == 0:
        break
    else:
        for headline in res_soup_headlines:
                print(headline.text) #헤드라인
                article_link['links'].append(headline['href'])
                word_article_list, word_sentence_list, word_list, sentence_list = get_detail.get(headline['href'])
                for word in word_list:
                    if (len(word) > 1):
                        word_freq[word] += 1

                if (len(word_article_list) > 0):
                    fp_word_article_csv.write(word_article_list + "\n")

                if (len(word_sentence_list) > 0):
                    for words in word_sentence_list:
                        fp_word_sentence_csv.write(words + "\n")

                if (len(word_list) > 0):
                    for word in word_list:
                        if (word not in word_freq):
                            word_freq[word] = 1
                        else:
                            word_freq[word] += 1

                if (len(sentence_list) > 0):
                    for sentence in sentence_list:
                        fp_sentence_list_csv.write(sentence + "\n")

                article_link['amount'] += 1

for word, freq in word_freq.items():
    f.write(str(word) + ',' + str(freq) + '\n')

# fp_freq_word_json.close()
fp_sentence_list_csv.close()
fp_word_sentence_csv.close()
fp_word_article_csv.close()
f.close()


