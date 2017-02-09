#!/usr/bin/env python
# -*- coding:utf-8 -*-
#######################

import urllib2
# If you are using Python 3+, import urllib instead of urllib2
import json 

### Functions
def get_OdorPrediction(DateTime,water,rain,temp,odor):
  data =  {
        "Inputs": {

                "input1":
                {
                    "ColumnNames": ["DateTime", "Mwater", "Mrain", "Mtemp", "MH2S"],
                    "Values": [ [ DateTime, water, rain, temp, odor ] ]
                },        },
            "GlobalParameters": {
            }
  }

  body = str.encode(json.dumps(data))

  # 線形回帰
  url = 'https://japaneast.services.azureml.net/workspaces/5c7f4898c83345f1be12ded6bba2262b/services/463969db2b444e13ba90a6e233ed6480/execute?api-version=2.0&details=true'
  api_key = 'Nl9AFgkjItxmh973mAgIYejw3zODlqSTbYM8kK+avGSjwXJGPIbCLjfQBWCCMh4aCjiuyUC7pgeufierIKiaMQ==' # Replace this with the API key for the web service

  # ブートデシジョンツリー
##  url = 'https://ussouthcentral.services.azureml.net/workspaces/e6eea5dbbad8430c8cfdb5b7df3b4ccd/services/404c2e071a3045689a7d75810d279476/execute?api-version=2.0&details=true'
##  api_key = '3PHUHFyeo9TDSYJ2781TkZmHJthxMXvays6vmyKXRTFBqd3P9tM1IPXVpjpR6Q+yysGDvrJnWEmP7mnk7V9HWA=='
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

  req = urllib2.Request(url, body, headers) 

  try:
    response = urllib2.urlopen(req)

    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    # response = urllib.request.urlopen(req)

    result = response.read()
##    print(result) 
    return result
  except urllib2.HTTPError, error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())

    print(json.loads(error.read()))
