#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################
## 使い方
## megLogicMain.py $1 $2
## $1:経度 lat
## $2:緯度 lon
#######################
import getNowData as WetherNow
import getForecastData as WetherForec
import getOdorFromRaspai as OdorFromRaspai
import getWaterLvFromPytide as WaterLvForec
import getWaterLvFromJupyter as WaterLvPre
import setRiverData as RiverData
import actAzureMachineLearning as AzML
import spAddDuplicateDateTimeUpdateItem as RiverData2
from datetime import datetime
import csv
import json
import math
import sys
import string
import os
import warnings;warnings.filterwarnings('ignore')
import time

import pandas as pd

if __name__ == "__main__":

  ## 現在時刻
  ##nowdate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
  nowdate = datetime.now().strftime("%Y-%m-%d %H:%M")

  ## 観測地情報(固定)
  ObsrPoint = "Meguro River A"

  # 河川情報を取得
  ri_data = WetherNow.get_riverInfo()

  #  河川情報を一時ファイルに出力
  f = open('tmp','w')
  f.write(ri_data)
  f.close()

  # 水位データ
  ld = open("tmp")
  lines = ld.readlines()
  ld.close()

  i = 0
  targNum = 99999
  waterLevel = 0

  for line in lines:
    if line.find("現在の水位(cm)") >= 0:
      targNum = i + 2
    if i == targNum:
      waterLevel = line[:-1].strip()
    i = i + 1

  ###### A地点 ########################
  #### 東京都品川区西五反田3丁目6?23 ##
  #### 35.6273664 139.7189429        ##
  #####################################
  argvs = sys.argv
  lat=argvs[1]
  lon=argvs[2]

  json_str = WetherNow.act_OpenWeatherMap(lat, lon)
  wes_dataArry = json.loads(json_str)

  # ケルヴィン氏温度の絶対零度
  absl_temp = 273.15

  # 気温
  jp_temp = OdorFromRaspai.get_RaspiData("temp")

  # 臭気
  odor = OdorFromRaspai.get_RaspiData("odor")

  # 10分間雨量を取得(上目黒)
  rain_data = WetherNow.get_rainInfo()

  #  サイトの10分間雨量情報を一時ファイルに出力
  f = open('tmp2','w')
  f.write(rain_data)
  f.close() 

  # 10分間雨量データ
  ld = open("tmp2")
  lines = ld.readlines()
  ld.close()
  
  i = 0
  targNum = 99999
  Precip = 0
  for line in lines:
    if line.find("10分間雨量") >= 0:
      targNum = i + 1
    if i == targNum:
      tmpdata1 = line[:-1].strip()
      tmpdata2 = tmpdata1.replace("<td>","")
      tmpdata2 = tmpdata2.replace(" mm</td>","")
      Precip = tmpdata2
      ##Precip = line[:-1].strip()
    i = i + 1

  # 実測値の編集対象ファイル
  targDir = "/home/megadmin/data/"
  fileName = "real_data.txt"
  filePath = targDir + fileName

  # 実測値用テーブル
  nowtable = [nowdate,ObsrPoint,waterLevel,Precip,jp_temp,odor]

  # テキストへの出力
  wcsv_obj = csv.writer(file(filePath, 'a'), lineterminator='\n')
  wcsv_obj.writerow(nowtable)

  # Zabbix へ溜めておく
#  zbxf_waterLevel_path = "/home/megadmin/data/zabbix/zabbixdata_odor_real"
#  zf_obj = open(zbxf_waterLevel_path, 'w')

#  now=int()
#  nowunixtime = datetime.datetime.fromtimestamp(now)

#  wstr = "meguro-river-A_real " + "waterLevel " + str(nowunixtime) + " " + odor
#  zf_obj.write(wstr)
#  zf_obj.close()
#  zcmd = "sudo zabbix_sender -z 127.0.0.1 -p 10051 -T -i " + zbxf_waterLevel_path
#  a = subprocess.check_output( zcmd,shell=True )

  ### ポータルに実測値を送付
  ######################
  portalr = RiverData.set_RiverDataToPortal('RiverData','目黒川河川データ測定', nowdate, ObsrPoint, waterLevel, Precip, jp_temp, odor,0)
  
  ### 天気予報から未来データを取得
  json_str = WetherForec.act_OpenWeatherMap(lat, lon)
  wes_data = json.loads(json_str)  

  # 未来予測値の編集対象ファイル
  fileNameF = "forecast_data.txt"
  filePathF = targDir + fileNameF

  # 未来予測の編集

  i = 0
  for i in range(0,35):
    # 予報年月日と日時

    utc_unixtime = wes_data["list"][i]["dt"]
    jst_unixtime = utc_unixtime 
    date_time_frt = datetime.fromtimestamp(jst_unixtime)
    date_time = date_time_frt.strftime("%Y-%m-%d %H:%M")

    #予測 気温
    temperatureF = wes_data["list"][i]["main"]["temp"]
    jp_tempF = temperatureF - absl_temp
  
    # 予測水位(仮)
    waterLevelF = 9999

    # 予想降水量
    PrecipF = 0
    if wes_data["list"][i]["weather"][0]["main"] == "Rain":
      PrecipF = wes_data["list"][i]["rain"]["3h"]
    else:
      PrecipF = 0

    # 未来予測値テーブル
    Forectable = [date_time,ObsrPoint,waterLevelF,PrecipF,round(jp_tempF,2),odor]

    wcsv_objF = csv.writer(file(filePathF, 'a'), lineterminator='\n')
    wcsv_objF.writerow(Forectable)
    i += 1

  waterLevelF = WaterLvForec.get_WaterLevelForecast(date_time_frt.strftime("%Y-%m-%d %H:%M"),ObsrPoint)
  waterleveltmp_filenm = '/home/megadmin/data/waterleveltmp.txt'
  waterLevelF.to_csv(waterleveltmp_filenm)

  ######### test ##########
  odorF_test = WaterLvForec.get_OdorlForecast(date_time_frt.strftime("%Y-%m-%d %H:%M"),ObsrPoint)
  odortmp_filenm = '/home/megadmin/data/odortmp.txt'
  odorF_test.to_csv(odortmp_filenm)
  ########################

  # 記載済み予測ファイルの水位を修正
  forecdf = pd.read_csv(filePathF)

  # 水位予測ファイルのデータ取り込み
  tmpld = open(waterleveltmp_filenm)
  tmplines = tmpld.readlines()

  # 当該時間の予測ファイル
  ##fileNameF = "forecast_data.txt"
  newFilePathF0 = targDir + fileNameF + '_' + nowdate[0:17]
  newFilePathF1 = newFilePathF0.replace(" ","_")
  newFilePathF = newFilePathF1.replace(":","-")

  newForecFile = open(newFilePathF,"w")
  i = 0
  for thisline in forecdf.iterrows():
    thisdates = forecdf.iloc[i,0]
    for line in tmplines:
      if line.find(thisdates) >= 0:
        forecWaterlv = line[20:].rstrip("\n")

        ### Azure Machine Learning !!
        forecWaterlvR = round(float(forecWaterlv),0)

        thisOdor = AzML.get_OdorPrediction(forecdf.iloc[i,0],forecWaterlvR,int(forecdf.iloc[i,3]),int(forecdf.iloc[i,4]),forecdf.iloc[i,5])

        rstjson = json.loads(thisOdor)
        OdorScore = rstjson['Results']['output1']['value']['Values'][0][5]

        ### ポータルに予測値を送付
        ## portalr2 = RiverData.set_RiverDataToPortal('PredictionData','目黒川河川予測データ', forecdf.iloc[i,0], forecdf.iloc[i,1], forecWaterlv[:-9], forecdf.iloc[i,3], forecdf.iloc[i,4], str(OdorScore[:-10]),1)

        pre_chgdate_frt = forecdf.iloc[i,0]
#        pre_chgdate = datetime.strptime(pre_chgdate_frt,'%Y/%m/%d %H:%M')
        pre_chgdate = pre_chgdate_frt.replace("-","/")
#        print pre_chgdate

        portalr2 = RiverData2.set_RiverDataToPortal2('PredictionData','目黒川河川予測データ', pre_chgdate, forecdf.iloc[i,1], forecWaterlv[:-10], forecdf.iloc[i,3], forecdf.iloc[i,4], str(OdorScore[:-10]))

        thisdate = forecdf.iloc[i,0] + ',' + forecdf.iloc[i,1] + ',' + str(forecWaterlv)[:-10] + ',' + str(forecdf.iloc[i,3]) + ',' + str(forecdf.iloc[i,4]) + ',' + str(OdorScore[:-10]) + '\n'
        newForecFile.writelines(thisdate)
        thisdate = ""
        
    i += 1
  
  # ファイルクローズ
  newForecFile.close()
  tmpld.close()

  # 今回の予測データをリネームし保存
  ###os.rename(filePathF,newFilePathF)

  # 一時ファイルを削除する。
  os.remove(filePathF)
  os.remove('tmp')
  os.remove('tmp2')
