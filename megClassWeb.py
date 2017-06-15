#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
import json


#####################################
# Class’è‹`
#####################################
class ProxySet(object):
    def __init__(self):
        self.proxy_user = "z206R894"
        self.proxy_password = "mgmjoke4!"
        self.proxy_site = "131.248.58.101:8080"

# Functions
    def set_proxyURL(self, orgURL):

        setURL = 'http://' + self.proxy_user \
                + ':' + self.proxy_password \
                + "@" + self.proxy_site
        return setURL
