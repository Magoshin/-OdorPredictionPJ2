#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################

import json
import csv
import sys
import datetime

import pandas as pd
from pandas import DataFrame
from pandas import Series, read_csv, date_range

from pytides.tide import Tide
import numpy as np

### Functions
def get_WaterLevelForecast(foredate,place):

  historyFileNm="/megdata/data_meg-logic/real_data.txt"

  ## カラム名のサンプル #######################
  ## date,obsrPoint,waterLevel,precip,temp,odor
  #############################################

  df0 = pd.read_csv(historyFileNm ,index_col=0, parse_dates=True)
  water_level = df0['waterLevel']
  demeaned = water_level.values - water_level.values.mean()

  tide = Tide.decompose(demeaned, water_level.index.to_datetime())

  constituent = [c.name for c in tide.model['constituent']]
  df = DataFrame(tide.model, index=constituent).drop('constituent', axis=1)
##  df.sort('amplitude', ascending=False).head(10)

  # 今日の日付を取得
  today = datetime.datetime.today()
  # 翌日を取得
  # ※テスト用に５日後
  next_day = today + datetime.timedelta(days=5) 

  dates = date_range(start=today.strftime('%Y-%m-%d'), end=next_day.strftime('%Y-%m-%d'), freq='10T')
  hours = np.cumsum(np.r_[0, [t.total_seconds() / 3600.0 for t in np.diff(dates.to_pydatetime())]])
  times = Tide._times(dates[0], hours)
  prediction = Series(tide.at(times) + water_level.values.mean(), index=dates)

  return prediction

