#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################

import csv
import json
import math
import sys
import string
import subprocess
import linecache

### Functions
def get_RaspiData(key):
  keypass = '/home/megadmin/.ssh/id_rsa'
  ssh_user = 'pi@'
  rasPai_IP = '153.234.68.62'
  ##rasPai_IP = '153.155.221.31'

  cmd = "/usr/bin/ssh -o 'ConnectTimeout 1' -i " + keypass + " " + ssh_user + rasPai_IP + " 'python3 /home/pi/Documents/h2sSensor.py'"
  try:
    nowRaspiVal = subprocess.check_output( cmd,shell=True )
  except:
    histfile = '/home/megadmin/data/real_data.txt'
    num_lines = sum(1 for line in open(histfile))
    target_line = linecache.getline(histfile, int(num_lines))
    dummy_temp = target_line.split(',')[4]
    dummy_odor = target_line.split(',')[5]
    nowRaspiVal ="2016/12/24,12:00" + "," + dummy_temp + "," + dummy_odor

  nowRaspiValAry = nowRaspiVal.split(',')

  rtnData1 = nowRaspiValAry[2]
  rtnData2 = nowRaspiValAry[3].strip()

  if key == "temp":
    return str(rtnData1)
  elif key == "odor":
    return str(rtnData2)
  else:
    return str(rtnData1) + "," + str(rtnData2)
