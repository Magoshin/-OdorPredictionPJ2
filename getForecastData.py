#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import urllib
import urllib2
import json
import re
import datetime
import time

### Functions
def act_OpenWeatherMap(lat,lon):
  url = "http://api.openweathermap.org/data/2.5/forecast?"
  appid = '2e6469bef764db86ef2e3b5da3432002'
  params = urllib.urlencode(
              {'appid': appid,
               'lat': lat,
               'lon': lon,
              })
  response = urllib.urlopen(url+params)
  return response.read()
