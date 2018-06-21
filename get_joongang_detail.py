import requests
import json
from bs4 import BeautifulSoup
from konlpy.tag import Kkma
from konlpy.utils import pprint

def get(url):
    kkma = Kkma()
    req_url = str(url)

    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    req = requests.get(req_url, headers=req_headers)
    html = req.text
    header = req.headers
    status = req.status_code
    is_ok = req.ok
    soup = BeautifulSoup(html, 'html.parser')
    article_title = soup.select("#article_title")
    print(article_title[0].text)
    article_regdate = soup.select(".article_head > .clearfx > .byline > em")
    print(article_regdate[1].text)
    article_content = soup.select("#article_body")
    #print(article_content[0].text)
    word_list = list()
    word_list = kkma.nouns(article_content[0].text)
    return word_list
