# -*- coding: utf-8 -*-
import urllib.request
import datetime
import json
import pandas as pd

# 🔑 Coloca aqui a tua Service Key
ServiceKey = "5b2544edb60938a65649bea31d935184bba28f7350cd339a4ab03713c30c4f62"


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def main():
    jsonResult = []
    result = []

    print("<< 국내 입국한 외국인의 통계 데이터를 수집합니다. >>")

    nat_cd = input('국가 코드를 입력하세요(중국: 112 / 일본: 130 / 미국: 275) : ')
    nStartYear = int(input('데이터를 몇 년부터 수집할까요? : '))
    nEndYear = int(input('데이터를 몇 년까지 수집할까요? : '))
    ed_cd = "E"  # E: 입국, D: 출국

    jsonResult, result, natName, dataEND = getTourismStatsService(
        nat_cd, ed_cd, nStartYear, nEndYear
    )

    # 📁 Save CSV file
    columns = ["입국자국가", "국가코드", "입국연월", "입국자 수"]
    result_df = pd.DataFrame(result, columns=columns)

    filename = f"{natName}_{ed_cd}_{nStartYear}_{dataEND}.csv"
    result_df.to_csv(filename, index=False, encoding='cp949')

    print(f"\n파일 저장 완료: {filename}")


# -------------------------------
# GET TOURISM DATA
# -------------------------------
def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []

    natName = ""   # 🔧 fix
    dataEND = ""   # 🔧 fix

    for year in range(nStartYear, nEndYear + 1):
        for month in range(1, 13):
            yyyymm = f"{year}{month:02d}"

            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)

            if jsonData is None:
                continue

            if jsonData['response']['header']['resultMsg'] == 'OK':

                # ❗ if no more data
                if jsonData['response']['body']['items'] == '':
                    dataEND = f"{year}{month-1:02d}"
                    print(f"\n데이터 없음 → 마지막 데이터: {dataEND}")
                    break

                # Extract data
                item = jsonData['response']['body']['items']['item']

                natName = item['natKorNm'].replace(' ', '')
                num = item['num']

                print(f"[ {natName}_{yyyymm} : {num} ]")
                print('-----------------------------')

                jsonResult.append({
                    'nat_name': natName,
                    'nat_cd': nat_cd,
                    'yyyymm': yyyymm,
                    'visit_cnt': num
                })

                result.append([natName, nat_cd, yyyymm, num])

    return (jsonResult, result, natName, dataEND)


# -------------------------------
# CALL API
# -------------------------------
def getTourismStatsItem(yyyymm, nat_cd, ed_cd):
    service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"

    parameters = "?_type=json"
    parameters += "&serviceKey=" + ServiceKey
    parameters += "&YM=" + yyyymm
    parameters += "&NAT_CD=" + nat_cd
    parameters += "&ED_CD=" + ed_cd

    url = service_url + parameters

    responseDecode = getRequestUrl(url)

    if responseDecode is None:
        return None
    else:
        return json.loads(responseDecode)


# -------------------------------
# REQUEST FUNCTION
# -------------------------------
def getRequestUrl(url):
    req = urllib.request.Request(url)

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
# RUN
# -------------------------------
main()
