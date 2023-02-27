#!/usr/bin/env python3
# encoding: utf-8

import requests
import json
import time
from pprint import PrettyPrinter

import argparse as ap
parser = ap.ArgumentParser()
parser.add_argument('-i', required=False, default='localhost', type=str, help='host ip')
parser.add_argument('-p', required=False, default=50124, type=int)
parser.add_argument('-u', '--url', required=False, default='', type=str)
args = parser.parse_args()

urlbase = "http://{}:{}".format(args.i, args.p)

if len(args.url) > 0:
    urlbase = args.url
header_dict = {'Content-Type': 'application/json'}
pp = PrettyPrinter()
print = pp.pprint

# 1. health check
url = "{}/health".format(urlbase)
print(requests.get(url).json())

# 2. simulate direct message
url = "{}/direct_message".format(urlbase)
send_data = {
    "user_id": 50124,
    "user_name": "un1",
    "message_time": time.time(),
    "message_content": ""
}

# 2.1 jrrp
send_data["message_content"] = ",jrrp"
json_data = json.dumps(send_data)
r = requests.post(url, headers=header_dict, data=json_data, timeout=20000)
print(r.json())

# 2.2 rf
send_data["message_content"] = ",rf 10"
json_data = json.dumps(send_data)
r = requests.post(url, headers=header_dict, data=json_data, timeout=20000)
print(r.json())

# 2.3 rf + 说明
send_data["message_content"] = ",rf 10 测试"
json_data = json.dumps(send_data)
r = requests.post(url, headers=header_dict, data=json_data, timeout=20000)
print(r.json())

# 2.4 rfb 小数骰
send_data["message_content"] = ",rfb 10 1"
json_data = json.dumps(send_data)
r = requests.post(url, headers=header_dict, data=json_data, timeout=20000)
print(r.json())

# 2.4 rfb 大数骰
send_data["message_content"] = ",rfb 10 -2"
json_data = json.dumps(send_data)
r = requests.post(url, headers=header_dict, data=json_data, timeout=20000)
print(r.json())

# 3. simulate group message
url = "{}/group_message".format(urlbase)
send_data = {
    "user_id": 50124,
    "user_name": "un1",
    "message_time": time.time(),
    "message_content": ",jrrp"
}
json_data = json.dumps(send_data)
r = requests.post(url, headers=header_dict, data=json_data, timeout=20000)
print(r.json())