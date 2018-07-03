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

    article_result = ""
    result_sentence_list = list()
    result_word_list = list()
    print(status)
    if(status == 200):
        #print(html)
        soup = BeautifulSoup(html, 'html.parser')

        article_title = soup.select("#news_title_text_id")
        print(article_title)
        #print(article_title[0].text)
        article_regdate = soup.select(".news_date")
        print(article_regdate)
        #print(article_regdate[0].text)
        article_content = soup.select(".par")
        print(article_content)
        #print(article_content[0].text)
        if(len(article_content)>0):
            article_sentence_list = article_content[0].text.split(".")
            word_list = ""

            article_word_list = kkma.nouns(article_content[0].text)

            for word in article_word_list:
                if(len(word) >= 3):
                    article_result = article_result+word+","
                    result_word_list.append(word)
            print(article_result)

            for sentence in article_sentence_list:
                if(len(sentence)>0):
                    sentence_noun_list = kkma.nouns(sentence)
                    for noun in sentence_noun_list:
                        if(len(noun)>=3):
                            word_list = word_list +noun+","
                            result_sentence_list.append(word_list)
                    word_list = ""
            print(result_sentence_list)
    return article_result, result_sentence_list, result_word_list
