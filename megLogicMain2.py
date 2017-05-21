#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################
## 使い方 
## megLogicMain.py $1 
## $1:計測地点名
#######################
import getNowData as WetherNow
import getForecastData as WetherForec
import getOdorFromRaspai as OdorFromRaspai
import getWaterLvFromPytide as WaterLvForec
import actScikitLearn as ScikitlML
##import getWaterLvFromJupyter as WaterLvPre

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
  nowdate = datetime.now().strftime("%Y-%m-%d %H:%M")

  ## 観測地情報(引数から取得)
  argvs = sys.argv
  ObsrPoint = argvs[1]

  ################################################
  # pointDataFile.txt から観測地点情報を取得する。
  # 地点名,緯度,経度,降雨量取得先URL,水位取得先URL
  ################################################
  pointDataFile_path = "/home/megadmin/MeguroRiverPJ2/pointDataFile.txt"
  with open(pointDataFile_path,"rb") as point_f:
    reader = csv.reader(point_f)
    for row in reader:
      if row[0] == ObsrPoint:
        lat=row[1]
        lon=row[2]
        waterLevelURL=row[3]
        rainDataURL=row[4]

  # 河川情報Webサイトから現在の水位を取得
  waterLevel = WetherNow.get_riverInfo(waterLevelURL)

  # OpenWeatherMapからお天気情報取得
  json_str = WetherNow.act_OpenWeatherMap(lat, lon)

  wes_dataArry = json.loads(json_str)

  # ケルヴィン氏温度の絶対零度
  absl_temp = 273.15

  # 気温
  jp_temp = OdorFromRaspai.get_RaspiData("temp")

  # 臭気
  odor = OdorFromRaspai.get_RaspiData("odor")

  # 10分間雨量を取得(上目黒)
  Precip = WetherNow.get_rainInfo(rainDataURL,10)

  # 実測値の編集対象ファイル
  targDir = "/home/megadmin/data/"
  fileName = "real_data.txt"
  filePath = targDir + fileName

  # 実測値用テーブル
  nowtable = [nowdate,ObsrPoint,waterLevel,Precip,jp_temp,odor]

  # テキストへの出力
  wcsv_obj = csv.writer(file(filePath, 'a'), lineterminator='\n')
  wcsv_obj.writerow(nowtable)

  ### meg-portに実測値を送付
  ######################
  ## 2017/05/19 meg-portは改修中の為、この操作は行わず。
  ##portalr = RiverData.set_RiverDataToPortal('RiverData','目黒川河川データ測定', nowdate, ObsrPoint, waterLevel, Precip, jp_temp, odor,0)
  
  # 天気予報から未来データを取得
  json_str = WetherForec.act_OpenWeatherMap(lat, lon)
  wes_data = json.loads(json_str)  

  # 未来予測値の編集対象ファイル
  fileNameF = "forecast_data.txt"
  filePathF = targDir + fileNameF

  # 未来予測の編集

  i = 0
  for i in range(0,35):
    # 予報年月日と日時
    date_time_frt = datetime.fromtimestamp(wes_data["list"][i]["dt"])
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

        ### scikit-learn Machine Learning !!
        forecWaterlvR = round(float(forecWaterlv),0)

        thisOdor = ScikitlML.get_OdorPrediction(forecdf.iloc[i,0],forecWaterlvR,int(forecdf.iloc[i,3]),int(forecdf.iloc[i,4]),forecdf.iloc[i,5])

        OdorScore = thisOdor[0]

        pre_chgdate_frt = forecdf.iloc[i,0]
        pre_chgdate = pre_chgdate_frt.replace("-","/")

##2017/05/19 meg-portは改修中の為、この操作は行わず。
##        portalr2 = RiverData2.set_RiverDataToPortal2('PredictionData','目黒川河川予測データ', pre_chgdate, forecdf.iloc[i,1], forecWaterlv[:-10], forecdf.iloc[i,3], forecdf.iloc[i,4], str(OdorScore[:-10]))

        thisdate = forecdf.iloc[i,0] + ',' + forecdf.iloc[i,1] + ',' + str(forecWaterlv)[:-10] + ',' + str(forecdf.iloc[i,3]) + ',' + str(forecdf.iloc[i,4]) + ',' + str(OdorScore) + '\n'
        newForecFile.writelines(thisdate)
        thisdate = ""
        
    i += 1
  
  # ファイルクローズ
  newForecFile.close()
  tmpld.close()

  # 今回の予測データをリネームし保存
  ###os.rename(filePathF,newFilePathF)


