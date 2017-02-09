#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################
## 使い方
## getNowData.py lat lon
## lat : 経度
## lon : 緯度
## mode : 表示モード（0:zabbix_sender 1:print）
#######################

import sys
import urllib
import urllib2
import json
import re
import datetime
import time
import subprocess
import re
import linecache

### Functions
def get_riverInfo():
  url = "http://www.kasen-suibo.metro.tokyo.jp/im/uryosuii/tsim0106g_2B09.html"
  response = urllib2.urlopen(url)
  charset = response.headers.getparam('charset')
  html = response.read()
  if charset != '':
    try:
      codecs.lookup(charset)
      html = html.decode(charset, 'replace')
    except:
      pass

  for m in re.finditer(r'現在 (.*)$', html):
    print m.groups(1)


  targindex = html.find("現在の水位")
  
  return html

def act_OpenWeatherMap(lat, lon):
  url = "http://api.openweathermap.org/data/2.5/weather?"
  appid = '2e6469bef764db86ef2e3b5da3432002'

  params = urllib.urlencode(
              {'appid': appid,
               'lat': lat,
               'lon': lon,
              })
  response = urllib.urlopen(url+params)
  return response.read()

def get_rainInfo():
  url = "http://www.kasen-suibo.metro.tokyo.jp/im/popup/popup02_1B06.html"
  response = urllib2.urlopen(url)
  charset = response.headers.getparam('charset')
  html = response.read()
  if charset != '':
    try:
      codecs.lookup(charset)
      html = html.decode(charset, 'replace')
    except:
      pass

  return html

