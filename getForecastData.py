#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import urllib
import urllib2
import json
import re
import datetime
import time

from megClassWeb import ProxySet

### Functions
def act_OpenWeatherMap(lat,lon):

  url = "http://api.openweathermap.org/data/2.5/forecast?"
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
