import requests
import json
from bs4 import BeautifulSoup
# from konlpy.tag import Kkma
from konlpy.tag import Twitter
# import Apriori as apriori

def get(url):
    twitter = Twitter()
    req_url = str(url)

    req_header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.' }
    res = requests.get(req_url, headers=req_header)
    res.encoding='euc-kr' # 경향신문 인코딩
    status = res.status_code

    html = res.content

    split_sentence_list = list()  # 기사 문장 분리 리스트
    beauty_sentence_list = list()  # 수정 문장 리스트
    article_words = ""  # 기사 단위 단어
    sentence_words = ""  # 문장 단위 단어
    sentence_words_list = list()  # 문장 단위 단어 리스트
    article_word_list = list()  # 빈도수 체크용 단어 리스트

    if (status == 200) :

        soup = BeautifulSoup(html, 'html.parser')
        article_content_all = soup.select(".art_body > p.content_text")  # 경향신문
        article_content = ""

        for paragraph in article_content_all:  # 경향신문은 문단별로 텍스트가 나뉘어 있음
            article_content += paragraph.text + "\n"

        if (len(article_content) > 0):
            split_sentence_list = article_content.split(".")  # 기사 문장 단위 분리

            for sentence in split_sentence_list:  # 문장 리스트 생성
                if (len(sentence) > 15):  # 문장 길이 제한
                    beauty_sentence = sentence.replace("\n", "")  # 개행 문자 제거
                    beauty_sentence = sentence.replace(",", " ")     # 컴마 제거
                    beauty_sentence = beauty_sentence.replace("\t", "")  # 탭 문자 제거
                    beauty_sentence_list.append(beauty_sentence)  # 문장 리스트에 추가

        __article_word_list = twitter.nouns(article_content)  # 기사 전체 단어 분리

        for word in __article_word_list:  # 기사 단위 단어 저장
            if (len(word) >= 3):  # 단어 길이 제한(3자 이상)
                article_words += word + ","  # 기사 단위 단어 스트링 생성
                article_word_list.append(word)  # 빈도수 체크용 단어 리스트에 단어 추가

        for sentence in split_sentence_list:  # 문장 단위 단어 저장
            sentence_words = ""  # 문장 단위 단어 스트링 초기화
            if (len(sentence) > 15):  # 문장 길이 제한
                __sentence_word_list = twitter.nouns(sentence)  # 문장 단위 단어 분리
                for word in __sentence_word_list:
                    if (len(word) >= 3):  # 단어 길이 제한
                        sentence_words = sentence_words + word + ","  # 문장 단위 단어 스트링 생성
                sentence_words_list.append(sentence_words)  # 문장 단위 단어 스트링 리스트 추가

    return article_words, sentence_words_list, article_word_list, beauty_sentence_list