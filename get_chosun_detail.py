import requests
from bs4 import BeautifulSoup
from konlpy.tag import Kkma

def get(url):
    kkma = Kkma()
    req_url = str(url)

    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    req = requests.get(req_url, headers=req_headers)
    html = req.content
    header = req.headers
    status = req.status_code
    is_ok = req.ok
    print(status)

    split_sentence_list = list() # 기사 문장 분리 리스트
    beauty_sentence_list = list() # 수정 문장 리스트
    article_words = "" # 기사 단위 단어
    sentence_words = "" # 문장 단위 단어
    sentence_words_list = list() # 문장 단위 단어 리스트
    article_word_list = list() # 빈도수 체크용 단어 리스트

    if(status==200):
        soup = BeautifulSoup(html, 'html.parser')

        article_title = soup.select("#news_title_text_id") # 기사 제목
        article_regdate = soup.select(".news_date") # 기사 등록일
        article_content = soup.select(".par") # 기사 본문

        if(len(article_content)>0):
            split_sentence_list = article_content[0].text.split(".") # 기사 문장 단위 분리

            for sentence in split_sentence_list: # 문장 리스트 생성
                if(len(sentence)>15): # 문장 길이 제한
                    beauty_sentence = sentence.replace("\n", "") # 개행 문자 제거
                    beauty_sentence = beauty_sentence.replace("\t", "") # 탭 문자 제거
                    beauty_sentence_list.append(beauty_sentence) # 문장 리스트에 추가

        __article_word_list = kkma.nouns(article_content[0].text) #기사 전체 단어 분리

        for word in __article_word_list: #기사 단위 단어 저장
            if(len(word) >= 3): # 단어 길이 제한
                article_words = article_words+word+"," # 기사 단위 단어 스트링 생성
                article_word_list.append(word) # 빈도수 체크용 단어 리스트에 단어 추가

        for sentence in split_sentence_list: #문장 단위 단어 저장
            sentence_words = "" # 문장 단위 단어 스트링 초기화
            if(len(sentence) > 15): # 문장 길이 제한
                __sentence_word_list = kkma.nouns(sentence) # 문장 단위 단어 분리
                for word in __sentence_word_list:
                    if(len(word) >= 3): # 단어 길이 제한
                        sentence_words = sentence_words+word+"," # 문장 단위 단어 스트링 생성
                sentence_words_list.append(sentence_words) # 문장 단위 단어 스트링 리스트 추가

    return article_words, sentence_words_list, article_word_list, beauty_sentence_list




