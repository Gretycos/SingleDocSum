# -*- coding:utf-8 -*-
import requests
import json

import logging
logger = logging.getLogger(__name__)

API_KEY = "2K3w5gfNF8YeqreUCoYrRI3q"
SECRET_KEY = "lGVVE8h1iSdOLQeNZeHdzLpssQl25kx6"
HOST = "aip.baidubce.com"
header = {
    "content-type": "application/json;charset=utf-8",
    "Host": HOST
}


def getAccessToken():
    logger.info("正在获取AccessToken...")
    URI = "/oauth/2.0/token"

    params = {
        'grant_type': "client_credentials",
        'client_id': API_KEY,
        'client_secret': SECRET_KEY
    }
    paramsList = [key + "=" + value for key,value in params.items()]
    UrlParams = '&'.join(paramsList)
    url = "https://" + HOST + URI + "?" + UrlParams
    r = requests.post(url, headers=header)
    access_token = r.json()['access_token']
    logger.info("获取AccessToken成功: {}".format(access_token))
    return access_token

def getSummary(access_token,title,content,max_summary_len):
    logger.info("正在获取摘要...")
    URI = "/rpc/2.0/nlp/v1/news_summary"

    params = {
        'charset': "UTF-8",
        'access_token': access_token
    }
    body = {
        'title': title,
        'content': content,
        'max_summary_len': max_summary_len
    }
    paramsList = [key + "=" + value for key, value in params.items()]
    UrlParams = '&'.join(paramsList)
    url = "https://" + HOST + URI + "?" + UrlParams
    r = requests.post(url, headers=header,data=json.dumps(body))
    try:
        summary = r.json()['summary']
        return summary
    except Exception as e:
        logger.error("获取主题失败: {}".format(e))

