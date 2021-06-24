# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : 3rd_Project.py & Last Modded : 2021.04.16. ###
Coded with Python 3.9 for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import os
import math
import winAPI
from covidAPI.covidinf import *


def printDict(dictdata, indent=0, color=0, color_on=True):
    """딕셔너리 자료형을 입력받아 전부 출력합니다.
       딕셔너리의 value로 딕셔너리가 있으면 재귀적으로 내부까지 출력합니다.
       1차원의 튜플(값, 퍼센트)이 value인 경우에도 출력 가능합니다.
       indent에 값을 입력하면 들여쓰기가 가능합니다.(indent level당 공백 2칸)"""
    for key, value in dictdata.items():
        winAPI.gotoXY(indent*2, winAPI.wrIsY())
        if color_on: winAPI.changeTxtColor((color+2) % 16)
        print(key, end=' : ')
        winAPI.gotoXY(winAPI.wrIsX(), winAPI.wrIsY()+1)
        winAPI.gotoXY(winAPI.wrIsX(), winAPI.wrIsY()-1)
        if (type(value) == dict):
            print()
            printDict(value, indent+1, color+1, color_on)
        elif (type(value) == tuple):
            winAPI.gotoXY(indent*2, winAPI.wrIsY())
            print(value[0])
            winAPI.gotoXY(indent*2+len(key)+6+len(value[0]), winAPI.wrIsY()-1)
            if color_on: winAPI.changeTxtColor((color+3) % 16)
            print(value[1])
        else:
            winAPI.gotoXY(indent*2, winAPI.wrIsY())
            if color_on: winAPI.changeTxtColor((color+2) % 16)
            print(value)
    if color_on: winAPI.changeTxtColor(winAPI.colorset['흰색'])


def printTuple(tupledata, indent=0, color=0, color_on=True):
    """튜플 자료형을 입력받아 내부 자료형까지 전부 출력합니다.
       딕셔너리의 value로 딕셔너리가 있으면 재귀적으로 내부까지 출력합니다.
       indent에 값을 입력하면 들여쓰기가 가능합니다.(indent level당 공백 2칸)"""
    for value in tupledata:
        winAPI.gotoXY(indent*2, winAPI.wrIsY())
        if color_on: winAPI.changeTxtColor((color+2) % 16)
        if type(value) == dict:
            printDict(value, indent, color, color_on)
        elif type(value) == dict_ext:
            cp = value.copy()
            print(cp.pop('항목'))
            printDict(cp, indent+1, color+1, color_on)
            print()
        elif type(value) == tuple:
            printTuple(value, indent, color, color_on)
        elif type(value) == VaccineCenter:
            print(value.name)
            if color_on: winAPI.changeTxtColor((color+3) % 16)  # 색 오류가 있는데 뭐가 문제인지 모르겠다.
            winAPI.gotoXY((indent+1)*2, winAPI.wrIsY())
            print("센터유형 : " + value.type)
            winAPI.gotoXY((indent+1)*2, winAPI.wrIsY())
            print("운영기관 : " + value.operator)
            winAPI.gotoXY((indent+1)*2, winAPI.wrIsY())
            print("시설명   : " + value.alias)
            winAPI.gotoXY((indent+1)*2, winAPI.wrIsY())
            print("우편번호 : " + value.zipcode)
            winAPI.gotoXY((indent+1)*2, winAPI.wrIsY())
            print("주소     : " + value.address, end='\n\n')
        else:
            print(value)
    if color_on: winAPI.changeTxtColor(winAPI.colorset['흰색'])


def printDataByColumns(inf, col=3, obj=dict, lineup=True):
    """데이터를 2열 혹은 3열로 나누어 출력한다. 기본값은 3열"""
    printObj = printTuple if obj == tuple else printDict
    div = inf if obj == tuple else list(inf.items())
    token = math.ceil(len(inf)/col)
    before = winAPI.wrIsY()
    printObj(obj(div[0:token]))
    after = winAPI.wrIsY()
    winAPI.gotoXY(0, before)
    if col == 3:
        printObj(obj(div[token:token*2]), indent=20)
        winAPI.gotoXY(0, before)
        printObj(obj(div[token*2:]), indent=40)
    else:
        printObj(obj(div[token:]), indent=20 if lineup else 30)
    winAPI.gotoXY(0, after+2)


def showBriefWindow(caseTable):
    """메인 화면을 출력합니다. 간단한 코로나 상황도 알려줍니다."""
    os.system("cls")
    print("현재 코로나 상황\n\n")
    printDict(caseTable)
    winAPI.gotoXY(30, 3)
    print("1. 시도별 코로나 현황")
    winAPI.gotoXY(30, 5)
    print("2. 국가별 코로나 현황")
    winAPI.gotoXY(30, 7)
    print("3. 성별, 연령대별 코로나 현황")
    winAPI.gotoXY(30, 9)
    print("4. From CSV")
    winAPI.gotoXY(30, 11)
    return input("데이터 종류 선택 : ")


def showSidoWindow(inf):
    """시도별 데이터 관련입니다."""
    os.system("cls")
    printDataByColumns(inf)
    try:  # 검색 1회 실행
        printDict(inf[input("시도별 데이터 전체입니다.\n검색할 지역을 입력하세요 : ")])
        print("\n\n")
    except Exception:
        print("검색 결과가 없습니다.\n\n")
    checkSidoGrades(inf)
    os.system("pause")


def checkSidoGrades(inf):
    """1. 가장 등급이 높은 지역들을 찾고, 해당 지역들에 비해 비교적 안전한 지역의 목록을 set의 연산들로 구현합니다.
       2. 신규확진자수가 15명 이상인 지역들을 찾고 1에서의 위험 지역와 비교합니다."""
    max = '0'
    citys = set(inf.keys())
    danger = set()
    for city, value in inf.items():
        if max < value['grade']:
            max = value['grade']
            danger.clear()
            danger.add(city)
        elif max == value['grade']:
            danger.add(city)
    not_danger = citys - danger
    print("현재 거리두기 최고 등급 " + max + " 단계인 위험한 지역은 아래와 같습니다 :")
    print(danger, end='\n\n')
    print("아래의 지역은 비교적 안전합니다 :")
    print(not_danger, end='\n\n')

    dif = set()
    std = '20'
    for city, value in inf.items():
        if int(std) <= int(value['diff']):
            dif.add(city)
    print("신규 확진자 수가 " + std + "명 이상인 지역은 아래와 같습니다 :")
    print(dif, end='\n\n')
    print("아래의 지역은 거리두기 등급이 높으면서 신규 확진자 수가 " + std + "명 이상인 지역입니다 :")
    print(danger & dif)


def showWorldWideWindow(inf_n, inf_w):
    """국가별 데이터 관련입니다. 간단한 국제 코로나 상황도 알려줍니다."""
    os.system("cls")
    printDataByColumns(inf_n)
    tmp = winAPI.wrIsY()
    winAPI.gotoXY(80, tmp)
    print("세계 코로나 상황")
    winAPI.gotoXY(80, tmp+2)
    printDict(inf_w, 40)
    winAPI.gotoXY(0, tmp)
    try:  # 검색 1회 실행
        printDict(inf_n[input("국가별 데이터 조회가 가능합니다.\n검색할 국가를 입력하세요 : ")])
        print("\n\n")
    except Exception:
        print("검색 결과가 없습니다.\n\n\n\n")
    os.system("pause")
    winAPI.gotoXY(0, winAPI.wrIsY()-1)
    checkDangerNation(inf_n)

    os.system("pause")


def checkDangerNation(inf):
    """코로나 상태가 심각한 국가들을 출력합니다."""
    patient = (set(), set())
    death = (set(), set())
    rate = set()
    for nat, val in inf.items():
        if int(val['patient_cnt'].replace(',', '')) >= 2000000:
            patient[0].add(nat)
            patient[1].add(val['continent'])
        if int(val['death_cnt'].replace(',', '')) >= 100000:
            death[0].add(nat)
            death[1].add(val['continent'])
        if float(val['death_percent']) >= 5:
            rate.add(nat)
    print("아래는 환자수가 많은 국가와 대륙입니다 :")
    print(patient[0])
    print(patient[1], end='\n\n')
    print("\n아래는 사망자수가 많은 국가와 대륙입니다 :")
    print(death[0])
    print(death[1], end='\n\n')
    print("\n아래는 사망률이 높은 국가입니다 :")
    print(rate, end='\n\n\n')
    print("아래는 환자수가 많거나 사망자수가 많은 국가와 대륙입니다 :")
    print(patient[0] | death[0])
    print(patient[1] | death[1], end='\n\n')
    print("아래는 환자수가 많고 사망자수도 많은 국가와 대륙입니다 :")
    print(patient[0] & death[0])
    print(patient[1] & death[1], end='\n\n')


def showGenAgeWindow(inf_g, inf_a):
    """성별, 나이대별 데이터 관련입니다."""
    os.system("cls")
    print("아래는 성별 데이터입니다.\n")
    printDataByColumns(inf_gender, 2)
    print("아래는 나이대별 데이터입니다.\n")
    printDataByColumns(inf_age)
    os.system("pause")
    winAPI.gotoXY(0, winAPI.wrIsY()-1)
    checkDangerAge(inf_a)

    os.system("pause")


def checkDangerAge(inf):
    """연령대 중 코로나 고위험군을 판단합니다."""
    patient = set()
    death = set()
    for age, val in inf.items():
        if float(val['확진자(%)'][1].replace('(', '').replace(')', '')) >= 11.11:
            patient.add(age)
        if float(val['사망자(%)'][1].replace('(', '').replace(')', '')) >= 11.11:
            death.add(age)
    print("아래는 확진자 비율이 높은 연령대입니다 :")
    print(patient, end='\n\n')
    print("아래는 사망자 비율이 높은 연령대입니다 :")
    print(death, end='\n\n')
    print("아래의 연령대는 코로나 고위험군입니다 :")
    print(patient & death, end='\n\n')


def showCsvWindow(csvlist, csvdata):
    """CSV로 불러온 자료들 관련입니다."""
    os.system("cls")
    for i in range(len(csvdata)):
        print(csvlist[1][i])
        if "예방접종센터" in csvlist[1][i]:
            viewCovidCenter(csvdata[i])
        elif "감정 변화" in csvlist[1][i]:
            viewCovidInducedEmoChanges(csvdata[i])
        elif "사회에 대한 전망" in csvlist[1][i]:
            viewPostCovidProspects(csvdata[i])
        else:
            printDataByColumns(csvdata[i], 2, tuple)
        os.system("pause")
        winAPI.gotoXY(0, winAPI.wrIsY()-1)


class VaccineCenter():
    """예방접종센터 데이터 보관용 클래스입니다.
    make(self, columns, values, skip_on=False, skip=None) 메소드가 존재합니다."""
    def __init__(self):
        super(VaccineCenter, self).__init__()
        self.type = ""
        self.name = ""
        self.operator = ""
        self.alias = ""
        self.zipcode = ""
        self.address = ""

    def make(self, columns, values, skip_on=False, skip=None):
        """columns과 values의 길이는 같아야 합니다."""
        data = []
        for col, val in zip(columns, values):
            find = False
            if skip_on:
                for sk in skip:
                    if col == sk:  # col is sk 사용 불가능 : 서로 다른 객체일 수 있음
                        find = True
                        break
                if find: continue
            data.append(val)
        if len(data) != 6:
            raise Exception("VaccineCenter 클래스의 멤버 메소드 make에서 오류가 발생했습니다.")
        self.type = data[0]
        self.name = data[1]
        self.operator = data[2]
        self.alias = data[3]
        self.zipcode = data[4]
        self.address = data[5]
        return self


def viewCovidCenter(inf):
    """현재 한국에 있는 예방접종 센터의 정보를 보여준다."""
    printDataByColumns(inf, 2, tuple, False)
    try:  # 검색 1회 실행
        qur = input("예방접종센터 조회가 가능합니다.\n검색어를 입력하세요 : ")
        found = False
        for data in inf:
            if qur in data.name:
                printTuple((data, ))
                found = True
        assert found, "검색 결과가 없습니다.\n\n"
    except AssertionError as e:
        print(e)


def viewCovidInducedEmoChanges(inf):
    """자료에 있는 감정 별로 변화 양상에 대해 보여준다. 튜플안에 딕셔너리가 있는 자료를 불러와 화면에 출력한다."""
    printDataByColumns(inf, 2, tuple)
    os.system("pause")
    winAPI.gotoXY(0, winAPI.wrIsY()-1)
    emotion = set()
    for data in inf:
        if float(data['증가']) > 50:
            emotion.add(data['항목'])
    print("현재 한국인이 겪고 있는 감정은 아래와 같습니다 :")
    print(emotion, end='\n\n\n')


def viewPostCovidProspects(inf):
    """포스트 코로나 시대에 대한 사람들의 생각을 조사한 설문조사 결과를 불러온다.
       튜플 안에 딕셔너리가 있는 자료를 불러와 화면에 출력한다."""
    printTuple(inf)
    os.system("pause")
    winAPI.gotoXY(0, winAPI.wrIsY()-1)
    ans = [0, 0]
    for data in inf:
        if float(data['그렇다']) > 50:
            ans[0] += 1
        else:
            ans[1] += 1
    print("%d개의 설문항목을 제외한 %d개 항목에서 사람들은 '그렇다'고 답했습니다." % (ans[1], ans[0]), end='\n\n')


if __name__ == '__main__':
    os.system("TITLE 코로나 관련 정보 알리미 서비스")
    soup = returnSoup()
    caseTable = getCovid19Inf(soup)
    inf_sido = getCovid19SidoInf()
    inf_nation, inf_world = getCovid19NatInf()
    inf_gender, inf_age = getCovid19GenAgeCaseInf(soup)
    csvlist = getCsvList()
    csvdata = []
    for file in csvlist[1]:
        print(file, end='\n\n')
        if "예방접종센터" in file:
            try:
                vc = getCsvData(csvlist[0], file, encoding='euc_kr', obj=VaccineCenter, skip_on=True, skip=['연번'])
            except Exception:
                raise Exception("ERROR: 데이터를 불러오던 중 문제가 발생했습니다.\n" + file + "의 자료 구조가 적절하지 않습니다.")
            if vc is not None:
                csvdata.append(vc)
        else:
            res = getCsvData(csvlist[0], file, encoding='euc_kr')
            if res is not None:
                csvdata.append(res)
    print("데이터 불러오기를 완료하였습니다.")
    os.system("pause")

    while True:
        opt = showBriefWindow(caseTable)
        if opt == '1':
            showSidoWindow(inf_sido)
        elif opt == '2':
            showWorldWideWindow(inf_nation, inf_world)
        elif opt == '3':
            showGenAgeWindow(inf_gender, inf_age)
        elif opt == '4':
            showCsvWindow(csvlist, csvdata)
        else:
            break
    winAPI.gotoXY(0, 20)
    os.system("pause")
