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

  # $B@bL@JQ?t$r%;%C%H(B
  X = data.loc[:, ['waterLevel', 'precip', 'temp']].as_matrix()
  # $BL\E*JQ?t$r%;%C%H(B
  Y = data['odor'].as_matrix()

  # $BM=B,%b%G%k$r:n@.(B
  clf.fit(X, Y)

  # $B2s5"78?t$NCj=P(B
  a = clf.coef_
  # $B@ZJR(B ($B8m:9(B)$B$NCj=P(B
  b = clf.intercept_  

  """
  print a
  print b
  print clf.score(X, Y)
  """

  # $BJP2s5"JQ?t$r9~$a$k(B
  X2 = [water,rain,temp]
  
  # $BM=B,$r<B9T$7!"JQ?t$KF~$l$FJV$9!*!*(B
  forecOdor = clf.predict(X2)


  return forecOdor
