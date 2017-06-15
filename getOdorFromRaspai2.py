#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################
######################
# RasPi2号機用
#######################
import csv
import json
import math
import sys
import string
import subprocess
import linecache


# Functions
def get_RaspiData(key):

    keypass = '/home/megadmin/.ssh/id_rsa'
    ssh_user = 'pi@'

    rasPai_IP = '10.0.1.2'

    # dummy 処理にて待機中
    # rasPai_IP = '172.17.0.99'

    cmd = "/usr/bin/ssh -o 'ConnectTimeout 1' -i " + keypass \
        + " " + ssh_user + rasPai_IP \
        + " 'tail -n 1 /home/pi/iot/H2SppmXBee.log'"
    try:
        nowRaspiVal = subprocess.check_output(cmd, shell=True)
    except:
        histfile = '/megdata/data_meg-logic/real_data.txt'
        num_lines = sum(1 for line in open(histfile))
        target_line = linecache.getline(histfile, int(num_lines))
        dummy_temp = target_line.split(',')[4]
        dummy_odor = target_line.split(',')[5]
        nowRaspiVal = "2017/06/13,12:00,2,3,4,5" + "," + dummy_temp + "," + dummy_odor

    nowRaspiValAry = nowRaspiVal.split(',')

    rtnData1 = nowRaspiValAry[6]
    rtnData2 = nowRaspiValAry[7].strip()

    if key == "temp":
        return str(rtnData1)
    elif key == "odor":
        return str(rtnData2)
    else:
        return str(rtnData1) + "," + str(rtnData2)
