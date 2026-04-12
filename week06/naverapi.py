# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import datetime
import json

# 🔑 Coloca aqui as tuas chaves da Naver
client_id = "RU3Rk2lrnSjFBJxJ3KIx"
client_secret = "nn30rwZDp6"


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def main():

    node = 'news'  # tipo de busca (news, blog, etc.)
    srcText = input('검색어를 입력하세요: ')  # palavra de busca

    cnt = 0
    jsonResult = []

    # Primeira chamada da API
    jsonResponse = getNaverSearch(node, srcText, 1, 100)

    if jsonResponse is None:
        print("Erro na API")
        return

    total = jsonResponse['total']

    # Loop para pegar todas as páginas
    while ((jsonResponse is not None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)

        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)

    print(f'\n전체 검색 결과: {total} 건')

    # 📁 salvar arquivo JSON
    filename = f"{srcText}_naver_{node}.json"

    with open(filename, 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, ensure_ascii=False)
        outfile.write(jsonFile)

    print(f"저장 완료: {filename}")
    print(f"총 수집 데이터: {cnt} 건")


# -------------------------------
# SEARCH FUNCTION
# -------------------------------
def getNaverSearch(node, srcText, page_start, display):

    base = "https://openapi.naver.com/v1/search"
    node = f"/{node}.json"

    parameters = f"?query={urllib.parse.quote(srcText)}&start={page_start}&display={display}"

    url = base + node + parameters

    responseDecode = getRequestUrl(url)

    if responseDecode is None:
        return None
    else:
        return json.loads(responseDecode)


# -------------------------------
# REQUEST FUNCTION
# -------------------------------
def getRequestUrl(url):

    req = urllib.request.Request(url)python naverapi.py

    # 🔑 Add headers
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)

        if response.getcode() == 200:
            print(f"[{datetime.datetime.now()}] Url Request Success")
            return response.read().decode('utf-8')

    except Exception as e:
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")
        return None


# -------------------------------
# PROCESS DATA
# -------------------------------
def getPostData(post, jsonResult, cnt):

    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    # Convert date format
    pDate = datetime.datetime.strptime(
        post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900'
    )
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({
        'cnt': cnt,
        'title': title,
        'description': description,
        'org_link': org_link,
        'link': link,
        'pDate': pDate
    })


# -------------------------------
# RUN
# -------------------------------
main()