# -*- coding: utf-8 -*-


import os, sys
import csv, json
import glob
from urllib.request import urlopen
try:
    import requests
except Exception:
    if input("ERROR: requests 모듈이 설치되지 않았습니다. 설치할까요?(press y to install) : ") == 'y':
        os.system("pip install requests")
        import requests
    else:
        print("설치하지 않으시면 서비스 사용이 불가능합니다.")
        exit()
try:
    import html5lib
except Exception:
    if input("ERROR: html5lib 모듈이 설치되지 않았습니다. 설치할까요?(press y to install) : ") == 'y':
        os.system("pip install html5lib")
        import html5lib
    else:
        print("설치하지 않으시면 서비스 사용이 불가능합니다.")
        exit()
try:  # BeautifulSoup의 import 시점은 html5lib import 이후여야 함
    from bs4 import BeautifulSoup
except Exception:
    if input("ERROR: beautifulsoup4 모듈이 설치되지 않았습니다. 설치할까요?(press y to install) : ") == 'y':
        os.system("pip install beautifulsoup4")
        from bs4 import BeautifulSoup
    else:
        print("설치하지 않으시면 서비스 사용이 불가능합니다.")
        exit()

os.system("cls")


def getCovid19Inf(soup):
    """확진자 수 등 대표적인 수치만 불러옵니다. 파라미터로 BeautifulSoup의 리턴값이 필요합니다. return caseTable"""
    tag = soup.find('span', attrs={'class': 't_date'})
    print("감염 현황 데이터 조회 기준시 : " + tag.text)
    tags = soup.findAll('ul', attrs={'class': 'ca_body'})
    ca_value = [tag.dd.text for tag in tags]
    tags = soup.findAll('p', attrs={'class': 'inner_value'})
    inner_value = [tag.text for tag in tags]
    tags = soup.findAll('span', attrs={'class': 'txt_ntc'})
    txt_ntc = [tag.text for tag in tags]
    caseTable = {'확진환자': {'누적': ca_value[0], '전일대비': {'소계': inner_value[0], '국내발생': inner_value[1], '해외유입': [2]}},
                 '격리해제': {'누적': ca_value[1], '전일대비': txt_ntc[0]},
                 '격리중': {'누적': ca_value[2], '전일대비': txt_ntc[1]},
                 '사망': {'누적': ca_value[3], '전일대비': txt_ntc[2]}}
    return caseTable


def getCovid19SidoInf():
    """시도별 코로나 현황을 불러옵니다. return inf_sido, sido"""
    inf_json = json.load(urlopen("https://media-gw.naver.com/lambda/api/v1/web/media/covid19/covid19_api2.json?type=region"))['result']
    inf_sido = inf_json['regions']
    # inf_sido[0] = {'count': 누적 확진자, 'diff': 확진자수 변동, 'qurRate': 발생률, 'title': 지역 명, 'rate': 감염자 비율, 'url': 누리집}
    print("시도별 데이터 조회 기준시 : " + inf_json['infoMessage'])
    sido = {}
    flag = 0  # '검역' 데이터 삭제 위한 인덱스 저장용 변수
    for i in range(0, len(inf_sido)):
        if inf_sido[i]['title'] == '검역':
            flag = i  # 인덱스 저장
            continue
        sido[inf_sido[i]['title']] = i - (1 if flag else 0)  # 플래그가 켜지면 인덱스에서 -1
        #del inf_sido[i]['title']  # 지역명 삭제
        del inf_sido[i]['url']  # url 삭제
    del inf_sido[flag]  # 검역 삭제
    return inf_sido, sido


def getCovid19NatInf():
    """국가별 코로나 현황을 불러옵니다. return inf_nation, nations, world"""
    html = requests.get("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98").text
    soup = BeautifulSoup(html, 'html5lib')

    inf_json = json.load(urlopen("https://media-gw.naver.com/lambda/api/v1/web/media/covid19/covid19_api2.json?type=world"))['result']
    inf_nation = inf_json['nationList']
    # inf_sido[0] = {'active_cnt': 활성 감염자?, 'continent': 대륙, 'death_cnt': 사망자 수, 'death_diff': 신규 사망자, 'death_percent': 사망자 비율,
    #                'localInfection': 국소감염, 'nation_cd': 국가코드, 'nation_nm': 국가명, 'patient_cnt': 환자 수, 'patient_diff': 확진자수 변동}

    print("국가별 데이터 조회 기준시 : " + inf_json['infoMessage'])
    nations = {inf_nation[i].pop('nation_nm'): i for i in range(len(inf_nation))}
    world = {'patient_diff': soup.find('div', attrs={'class': 'status_info abroad_info'}).em.text,
             'patient_sum': soup.find('div', attrs={'class': 'status_info abroad_info'}).p.text,
             'death_diff': inf_json['death_diff'],
             'death_sum': inf_json['death_sum'],
             'death_percent': inf_json['death_percent']}
    return inf_nation, nations, world


def getCovid19GenAgeCaseInf(soup):
    """성별, 연령대별 코로나 현황을 불러옵니다. 파라미터로 BeautifulSoup의 리턴값이 필요합니다.
       return gender, age (괄호 안에 들어가있는 데이터는 퍼센트입니다.)"""
    tag = soup.find('span', attrs={'class': 't_date'})
    print("성별·연령별 현황 데이터 조회 기준시 : " + tag.text)
    tags = soup.findAll('div', attrs={'class': 'data_table'})
    tmp = [str(val) for tbody in tags[3].table.tbody for td in tbody for span in td for val in span if type(val) != type("")]
    gender = {'남성': {'확진자(%)': (tmp[0], tmp[1]), '사망자(%)' : (tmp[2], tmp[3]), '치명률': tmp[4]},
              '여성': {'확진자(%)': (tmp[5], tmp[6]), '사망자(%)' : (tmp[7], tmp[8]), '치명률': tmp[9]}}
    tmp = [str(val) for tbody in tags[4].table.tbody for td in tbody for span in td for val in span if type(val) != type("")]
    age = {}
    age_index = ('80이상', '70-79', '60-69', '50-59', '40-49', '30-39', '20-29', '10-19', '0-9')
    for i in range(9):
        age[age_index[i]] = {'확진자(%)': (tmp[i*5], tmp[i*5+1]), '사망자(%)' : (tmp[i*5+2], tmp[i*5+3]), '치명률': tmp[i*5+4]}
    return gender, age


def returnSoup():
    """html 파일을 여러 번 받아올 필요 없도록 BeautifulSoup의 반환값을 리턴해주는 함수. return soup"""
    html = requests.get("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun=").text
    soup = BeautifulSoup(html, 'html5lib')  # BeautifulSoup가 html5lib의 import 이후에 import 되어야 하는 이유
    return soup


def getCsvList(dir=os.path.dirname(os.path.realpath(__file__)) + "/CSV/"):
    # https://codechacha.com/ko/python-examples-get-working-directory/
    """__main__의 기준에서 하위 디렉토리 csv 안의 .csv 목록을 (경로, (파일명 튜플)) 형태로 불러옴.
       파라미터로 csv 파일 검색 경로 지정가능. (단, 디렉토리의 절대경로여야 한다.) return (dir, [])"""
#    try:
#        return dir, [fname for fname in os.listdir(dir) if len(fname) >= 4 and fname[-4] == '.' and fname[-3] == 'c' and fname[-2] == 's' and fname[-1] == 'v']
#    except FileNotFoundError:
#        print("ERROR : Wrong Directory", file=sys.stderr)
#        return dir, []
    return dir, tuple(os.path.basename(file) for file in glob.glob(dir + "*.csv"))


class dict_exp(dict):
    def make(self, columns, values, skip_on=False, skip=None):
        """columns과 values의 길이는 같아야 합니다."""
        for col, val in zip(columns, values):
            find = False
            if skip_on:
                for sk in skip:
                    if col == sk:  # col is sk 사용 불가능 : 서로 다른 객체일 수 있음
                        find = True
                        break
                if find: continue
            self[col] = val
        return self


def getCsvData(dir, fileName, encoding='utf-8', obj=dict_exp, skip_on=False, skip=None):
    """csv 파일을 읽어서 ({항목: 자료 객체}, ....)로 반환합니다.
       기본 인코딩은 utf-8이며 기본 자료 객체는 딕셔너리(dict_exp) 입니다.
       skip_on이 True이면 csv의 column 중 skip에 입력된 것을 생략할 수 있습니다.
       기본 자료 객체를 변경할 경우 클래스에는 make(self, columns, values, skip_on, skip) 함수가 있어야 합니다.
       파일이 존재하지 않는 경우 NoneType을 반환합니다."""
    try:
        file = open(dir + fileName, 'r', encoding=encoding)
        rdr = csv.reader(file)
        columns = next(rdr)
        res = tuple(obj().make(columns, row, skip_on, skip) for row in rdr)
        file.close()
        return res
    except FileNotFoundError:
        print("CSV OPEN ERROR : " + fileName, file=sys.stderr)


if __name__ == '__main__':
    soup = returnSoup()

    caseTable = getCovid19Inf(soup)
    for table in caseTable:
        print(table, end=' : ')
        print(caseTable[table])
    os.system("pause")
    os.system("cls")

    inf_sido, sido = getCovid19SidoInf()
    print(inf_sido[sido['대전']])  # 호출 예제
    for i in sido.values():
        print(inf_sido[i])
    os.system("pause")
    os.system("cls")

    inf_nation, nations, world = getCovid19NatInf()
    print(world)
    print(inf_nation[nations['한국']])  # 호출 예제
    for i in nations.values():
        print(inf_nation[i])
    os.system("pause")
    os.system("cls")

    gender, age = getCovid19GenAgeCaseInf(soup)
    print(gender)
    print()
    print(age)
    os.system("pause")
    os.system("cls")

    csvlist = getCsvList()
    csvdata = []
    for file in csvlist[1]:
        print(file)
        res = getCsvData(csvlist[0], file, encoding='euc_kr', skip_on=True, skip=['연번'])
        if res is not None:
            csvdata.append(res)
            for r in res:
                print(r)
            print()

    os.system("pause")
