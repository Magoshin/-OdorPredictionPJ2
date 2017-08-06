#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################
#######################

import sys
import requests
import json
import pandas
import pprint


# Functions
def sendRiverData(corection,
                  thisdate,
                  tide,
                  rainfall,
                  pressure,
                  cloudness,
                  windspeed,
                  temperature,
                  humidity,
                  H2S):

    megport_ip = "172.17.0.5"
    target_url = "http://" + megport_ip + "/api/" + corection

    response = requests.post(target_url, {'DateTime': thisdate,
                                          'tide': tide,
                                          'rainfall': rainfall,
                                          'pressure': pressure,
                                          'cloudness': cloudness,
                                          'windspeed': windspeed,
                                          'temperature': temperature,
                                          'humidity': humidity,
                                          'H2S': H2S})

    # pprint.pprint(response.json())

    return 0
