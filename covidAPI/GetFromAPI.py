# -*- coding: utf-8 -*-


import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from datetime import datetime

# read config file
from configparser import ConfigParser
config = ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/key.config")  # https://codechacha.com/ko/python-examples-get-working-directory/
API_KEY = config.get('dataportal', 'decodedkey')
END_DT = datetime.today().strftime('%Y%m%d')  # 현재 시점 데이터까지 불러오기
PARAMS = '?' + urlencode({quote_plus('ServiceKey') : API_KEY, quote_plus('pageNo') : '1', quote_plus('numOfRows') : '10', quote_plus('startCreateDt') : '20210331', quote_plus('endCreateDt') : END_DT})


if __name__ == '__main__':
    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'

    request = Request(url + PARAMS)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    print(response_body)

    os.system("pause")
