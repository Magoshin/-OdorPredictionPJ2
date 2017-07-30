#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################
######################
# RasPi からのデータ取得（全機共通）
#######################
import csv
import json
import math
import sys
import string
import subprocess
import linecache
import datetime
from megClassErrorLog import errorLog

# Functions
def get_RaspiData(key):

    # logfilepass = '/megdata/data_meg-logic/log/meg-logic.log'
    raspidata_tmp = '/megdata/data_meg-logic/raspidatatmp.txt'
    keypass = '/home/megadmin/.ssh/id_rsa'
    ssh_user = 'pi@'

    rasPai_IP = '10.0.1.1'

    cmd = "/usr/bin/ssh -o 'ConnectTimeout 5' -i " + keypass \
        + " " + ssh_user + rasPai_IP \
        + " 'tail -n 1 /home/pi/iot/H2Ssensor.log'"
    try:
        nowRaspiVal = subprocess.check_output(cmd, shell=True)
    except:
        histfile = '/megdata/data_meg-logic/real_data.txt'
        num_lines = sum(1 for line in open(histfile))
        target_line = linecache.getline(histfile, int(num_lines))
        dummy_temp = target_line.split(',')[4]
        dummy_humidity = target_line.split(',')[5]
        dummy_odor = target_line.split(',')[6].rstrip()

        nowRaspiVal = "Jul 28 13:10:18 2017" + "," \
            + dummy_odor + "," \
            + dummy_temp + "," \
            + dummy_humidity

    # 更新チェック用にデータを一時保存
    with open(raspidata_tmp, 'w') as raspitmp:
        raspitmp.write(nowRaspiVal)

    # RasPiから読み込んだデータ
    nowRaspiValAry = nowRaspiVal.split(',')

    # 1つ前のデータ
    with open(raspidata_tmp, 'r') as raspitmp:
        beforeRaspiVal = raspitmp.read()
    beforeRaspiValAry = beforeRaspiVal.split(',')

    # 更新エラー処理
    if nowRaspiValAry[0] == beforeRaspiValAry[0]:
        errObj = errorLog()
	thisModulePath = sys.argv[0].split('/')
	res = errObj.write_ErrorLog("E_Logic_0001", thisModulePath[3], "H2Ssensor.logが更新されていません。")

    # H2Ssensor.log
    # 0 : DateTime
    # 1 : H2S濃度 [ppb]
    # 2 : 気温 [℃]
    # 3 : 湿度 [％]
    rtnData1 = nowRaspiValAry[2]
    rtnData2 = nowRaspiValAry[1]
    rtnData3 = nowRaspiValAry[3].rstrip()

    if key == "temp":
        return str(rtnData1)
    elif key == "odor":
        return str(rtnData2)
    elif key == "humidity":
        return str(rtnData3)
    elif key == "all":
        return str(rtnData1) + "," + str(rtnData2) + "," + str(rtnData3)
    else:
        return str(rtnData1) + "," + str(rtnData2) + "," + str(rtnData3)
