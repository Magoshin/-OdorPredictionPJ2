#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################

from ipywidgets import FloatProgress
from IPython.display import display

#%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import datetime

### Functions
def get_WaterLevelJupyter(foredate,place):
  filename = "/home/megadmin/data/real_data.txt"
  df = pd.read_csv(filename, header=None)

  ##tmp = []
  ##for i in range(len(df)):
  ##  pos = len(df) - 1 - i
  ##  tmp.append(df.ix[pos][2])

  ##pd.DataFrame({'level': np.array(tmp)}).plot(figsize=(15,5))

  # データの開始日と終了日の取得
  dt1 = datetime.datetime.strptime(df[0][len(df)-1],"%Y-%m-%d %H:%M")
  dt1 = datetime.datetime(dt1.year,dt1.month,dt1.day,0,0)
  dt2 = datetime.datetime.strptime(df[0][0],"%Y-%m-%d %H:%M")

  return dt1
