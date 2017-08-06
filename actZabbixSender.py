#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import string
import subprocess
import linecache
import datetime

# Functions
def actZabbixSender(key, data):
        
    zabbix_server = "172.17.0.1"
    host = "meg-logic"
    cmd = "zabbix_sender -z " + zabbix_server + " -s " + host + " -k " + key + " -o " + data
    res = subprocess.check_output(cmd, shell=True)

    return res
