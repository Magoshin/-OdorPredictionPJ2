#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import datetime
import sys
import string

#####################################
# Class��`
#####################################
class errorLog(object):
    def __init__(self):
        self.logfilepass = "/megdata/data_meg-logic/log/meg-logic.log"

	d = datetime.datetime.today()
        self.todaystr = d.strftime("%Y-%m-%d %H:%M:%S")
# Functions
    def write_ErrorLog(self, code, moduleNm, msg):
        with open(self.logfilepass, 'a') as meglog:
            errmsg = self.todaystr + " " + moduleNm + " " + code + " " + msg + "\n"
            meglog.write(errmsg)

        return 0
