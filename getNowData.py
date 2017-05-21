#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################
## lat : 経度
## lon : 緯度
#######################

import sys
import urllib
import json
import pandas

from megClassWeb import ProxySet

### Functions
### 2 いきなり現在の水位がとれる様に改修
### 2 対象URLは引数でとる様に改修
def get_riverInfo(url):

  proxyObj = ProxySet()
  proxycode = proxyObj.set_proxyURL(url)
  proxy = {'http':proxycode}
  response = urllib.urlopen(url,proxies=proxy)

  html = response.read()

  fetched_dataframes = pandas.io.html.read_html(html)

  water_Level = fetched_dataframes[7].ix[1,1]

  return water_Level

def act_OpenWeatherMap(lat, lon):

  url = "http://api.openweathermap.org/data/2.5/weather?"

  proxyObj = ProxySet()
  proxycode = proxyObj.set_proxyURL(url)
  proxy = {'http':proxycode}

  appid = '2e6469bef764db86ef2e3b5da3432002'

  params = urllib.urlencode(
              {'appid': appid,
               'lat': lat,
               'lon': lon,
              })
  response = urllib.urlopen(url+params,proxies=proxy)

  return response.read()

## get_rainInfo(url,key)
## url:雨量の取得先URL
## key: 1 - 1分間雨量 10 - 10分間雨量
### 2 いきなり現在の水位がとれる様に改修
### 2 対象URLは引数でとる様に改修
def get_rainInfo(url,key):

  ##url = "http://www.kasen-suibo.metro.tokyo.jp/im/popup/popup02_1B06.html"

  proxyObj = ProxySet()
  proxycode = proxyObj.set_proxyURL(url)
  proxy = {'http':proxycode}

  response = urllib.urlopen(url,proxies=proxy)
  html = response.read()
  fetched_dataframes = pandas.io.html.read_html(html)
  
  if key == 1:
    rainfall = fetched_dataframes[0].ix[1,1]
  elif key == 10:
    rainfall = fetched_dataframes[0].ix[2,1]
  else:
    rainfall = "9999 mm"

  return rainfall.replace(' mm','')

