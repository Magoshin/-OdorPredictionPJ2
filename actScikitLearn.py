#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################

import json
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.externals import joblib

### Functions
def get_OdorPrediction(DateTime,water,rain,temp,odor):

  realFile = "/megdata/data_meg-logic/real_data.txt"
  data = pd.read_csv(realFile, sep=",")
  clf = linear_model.LinearRegression()

  # 説明変数をセット
  X = data.loc[:, ['waterLevel', 'precip', 'temp']].as_matrix()
  # 目的変数をセット
  Y = data['odor'].as_matrix()

  # 予測モデルを作成
  clf.fit(X, Y)

  # 回帰係数の抽出
  a = clf.coef_
  # 切片 (誤差)の抽出
  b = clf.intercept_  

  """
  print a
  print b
  print clf.score(X, Y)
  """

  # 偏回帰変数を込める
  X2 = [water,rain,temp]
  
  # 予測を実行し、変数に入れて返す！！
  forecOdor = clf.predict(X2)


  return forecOdor
