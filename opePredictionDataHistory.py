#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################

import json
import csv
import sys
import datetime
import subprocess
import os


# 観測地情報(引数から取得)
argvs = sys.argv
ObsrPoint = argvs[1]

# 今日の日付を取得
today = datetime.datetime.today()
yesterday = today - datetime.timedelta(days=1)
yesterdaystr = yesterday.strftime('%Y-%m-%d')

datadir = "/megdata/data_meg-logic"
targetfile = datadir + "/history/" + ObsrPoint + "_forecast_data.txt_" \
   + yesterdaystr + ".tgz "

if os.path.exists(targetfile):
    sys.exit()
else:
    try:
        cmd1 = "tar cvfz " \
             + datadir + "/" + ObsrPoint + "_forecast_data.txt_" \
             + yesterdaystr + ".tgz " + datadir \
             + "/" + ObsrPoint + "_forecast_data.txt_" + yesterdaystr + "*"
        r = subprocess.check_output(cmd1, shell=True)
        cmd2 = "mv " + datadir + "/" + ObsrPoint + "_forecast_data.txt_" \
               + yesterdaystr + ".tgz " + datadir + "/history/"
        print cmd2
        r = subprocess.check_output(cmd2, shell=True)
        cmd3 = "rm -fr " + datadir + "/" + ObsrPoint + "_forecast_data.txt_" \
               + yesterdaystr + "*"
        print cmd3
        r = subprocess.check_output(cmd3, shell=True)
    except Exception as e:
        print("message:", e.args)
