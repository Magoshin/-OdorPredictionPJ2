#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import json
import re
import datetime
import time

import requests
from requests.auth import HTTPBasicAuth

### Functions
def set_RiverDataToZBX(host,nowdate,obsrPoint,waterLevel,precip,jp_temp,odor):
  rtn = 0

  waterLevel = datatbl[2]
  Precip = datatbl[3]
  jp_temp = datatbl[4]
  odor = datatbl[5]
  
  return rtn

###############################################
## switchflag:  0:real data 1:forecast data
###############################################
def set_RiverDataToPortal(graphtype,title,thisdate,obsrPoint,waterLevel,precip,jp_temp,odor,switchflag):
  r = 0

  # SharePointのユーザIDとパスワードを設定
  sp_user = 'megadmin'
  sp_password = 'P@ssw0rdmeg!'

  # ShaerPointのリスト名を設定
  ##sp_listname = 'RiverData'
  sp_listname = graphtype

  # SharePonitのサイトのURL
  sp_url = 'http://meg-portal.japaneast.cloudapp.azure.com'

  # 基本認証
  auth = HTTPBasicAuth(sp_user,sp_password)

  # SharePointフォームダイジェスト値を取得
  headers = {
        "Accept":"application/json; odata=verbose",
        "Content-Type":"application/json; odata=verbose",
        "odata":"verbose",
        "X-RequestForceAuthentication":"true"
  }

  r = requests.post(sp_url + "/_api/contextinfo", auth=auth, headers=headers, verify=False)
  form_digest_value = r.json()['d']['GetContextWebInformation']['FormDigestValue']

  # SharePointリストにアイテムを追加
  headers = {
        "Accept":"application/json; odata=verbose",
        "Content-Type":"application/json; odata=verbose",
        "odata":"verbose",
        "X-RequestForceAuthentication":"true",
        "X-RequestDigest":form_digest_value,
  }
  # SharePointリストアイテムの型を定義
  sp_type = "SP.Data." + sp_listname + "ListItem"
  ### flag 処理入れる
  if switchflag == 0:
    data = {
          '__metadata': {'type':sp_type},
          'Title':title,
          'Location':obsrPoint,
          'DateTime':thisdate,
          'Mtemp':jp_temp,
          'MH2S':odor,
          'Mwater':waterLevel,
          'Mrain':precip
    }
  elif switchflag == 1:
    data = {
          '__metadata': {'type':sp_type},
          'Title':title,
          'Location':obsrPoint,
          'DateTime':thisdate,
          'Ptemp':jp_temp,
          'PH2S':odor,
          'Pwater':waterLevel,
          'Prain':precip
    }
  r = requests.post(sp_url + "/_api/web/lists/getbytitle('" + sp_listname + "')/items", data=json.dumps(data),auth=auth,headers=headers,verify=False)

  return r 
  # Response 201が帰ってきたらアイテムの追加に成功
  ##print r
  ##print sp_url + "/Lists/" + sp_listname
  #########################

