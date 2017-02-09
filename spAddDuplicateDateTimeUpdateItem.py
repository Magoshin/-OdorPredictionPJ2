#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#---------------------------------------------------------------------
# spAddDuplicateDateTimeUpdateItem.py ver0.1
#
# Usage       : spAddDuplicateDateTimeUpdateItem.py
# Project     : Prediction for bad smell around Meguro river
# Author      : shuichi.ikeda@ctc-g.co.jp
# Created     : Tue Jan 22 13:23:00 2017
# Copyright   : (c) 2017 Itochu Techno Solutions Corporation(CTC).
#---------------------------------------------------------------------

# coding:UTF-8
import requests
import json
from datetime import datetime
from requests.auth import HTTPBasicAuth
 
def set_RiverDataToPortal2(graphtype,title,thisdate,obsrPoint,waterLevel,precip,jp_temp,odor):
  # SharePointのユーザIDとパスワードを設定
  sp_user = 'megadmin'
  sp_password = 'P@ssw0rdmeg!'

  # SharePonitのサイトのURL
  sp_url = 'http://meg-portal.japaneast.cloudapp.azure.com'

  # SharePointのリスト名を設定
  sp_listname = graphtype

  # 予測日時
  dateTime = thisdate

  # SharePointのアイテム
  sp_item = {
      '__metadata': {'type':"SP.Data." + sp_listname + "ListItem"},
      'Title':title,
      'DateTime':dateTime,
      'Location':obsrPoint,
      'Pwater':waterLevel,
      'PH2S':odor
  }

  # SharePoint RESTを利用すためのヘッダー
  headers = {
      "Accept":"application/json; odata=verbose",
      "Content-Type":"application/json; odata=verbose",
      "odata":"verbose",
      "X-RequestForceAuthentication":"true",
  }

  # 基本認証
  auth = HTTPBasicAuth(sp_user,sp_password)

  # SharePointフォームダイジェスト値を取得
  r = requests.post(sp_url + "/_api/contextinfo", auth=auth, headers=headers, verify=False)
  form_digest_value = r.json()['d']['GetContextWebInformation']['FormDigestValue']

  # ISO形式の日時フォーマットに変換 (例：'2017/01/31 0:00' -> '2017-01-31T00:00:00')
  dateTimeISO = datetime.strptime(dateTime, '%Y/%m/%d %H:%M').isoformat() 

  # 予測日時のアイテムの有無を確認
  r = requests.get(sp_url + "/_api/web/lists/getbytitle('" + sp_listname + "')/items?$filter=DateTime eq datetime'" + dateTimeISO + "'", auth=auth, headers=headers, verify=False)
  items = r.json()['d']['results']

  # 予測日時のアイテムが無い場合は追加
  if len(items) == 0:
    # SharePointリストにアイテムを追加
    headers['X-RequestDigest'] = form_digest_value
    r = requests.post(sp_url + "/_api/web/lists/getbytitle('" + sp_listname + "')/items", data=json.dumps(sp_item),auth=auth,headers=headers,verify=False)
    # Response 201が帰ってきたらアイテムの追加に成功
    ##print r
    ##print sp_url + "/Lists/" + sp_listname + " ID:" + str(r.json()['d']['ID']) + " was added."
    
  # 予測日時のアイテムがある場合は更新
  else:
    # itemsの配列の最初のSharePointアイテムを更新
    headers['X-RequestDigest'] = form_digest_value
    headers['IF-MATCH'] = "*"
    headers['X-HTTP-Method'] = "MERGE"
    r = requests.post(sp_url + "/_api/web/lists/getbytitle('" + sp_listname + "')/items(" + str(items[0]['ID']) + ")", data=json.dumps(sp_item),auth=auth,headers=headers,verify=False)
    # Response 204が帰ってきたらアイテムの更新に成功
    ##print r
    ##print sp_url + "/Lists/" + sp_listname + " ID:" + str(items[0]['ID']) + " was updated."

    # 同一予測日時のアイテムが複数ある場合は削除
    # itemsの配列の2番目以降のSharePointアイテムを削除
    for item in items[1:]:
      headers['X-HTTP-Method'] = "DELETE"    
      r = requests.post(sp_url + "/_api/web/lists/getbytitle('" + sp_listname + "')/items(" + str(item['ID']) + ")", data=json.dumps(sp_item),auth=auth,headers=headers,verify=False)
      # Response 200が帰ってきたらアイテムの削除に成功
      ##print r
      ##print sp_url + "/Lists/" + sp_listname + " ID:" + str(item['ID']) + " was deleted."
    
    return r

