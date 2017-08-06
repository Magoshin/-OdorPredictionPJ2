#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import datetime
import sys
import string


#####################################
# Class’è‹`
#####################################
class errorLog(object):
    def __init__(self):
        self.logfilepass = "/megdata/data_meg-logic/log/meg-logic.log"
        self.raspilogpass = "/megdata/data_meg-logic/log/meg-logic-raspi.log"

        d = datetime.datetime.today()
        self.todaystr = d.strftime("%Y-%m-%d %H:%M:%S")

# Functions
    def write_ErrorLog(self, code, moduleNm, msg):
        with open(self.logfilepass, 'a') as meglog:
            errmsg = self.todaystr + " " \
                     + moduleNm + " " + code + " " + msg + "\n"
            meglog.write(errmsg)

        return 0

    def write_RaspiLog(self, msg):
        with open(self.raspilogpass, 'a') as meglog:
            raspimsg = self.todaystr + "," + msg + "\n"
            meglog.write(raspimsg)

        return 0
