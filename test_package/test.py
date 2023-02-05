#!/usr/bin/env python3
# encoding: utf-8

import requests
import json
import time

import argparse as ap
parser = ap.ArgumentParser()
parser.add_argument('-i', required=False, default='localhost', type=str, help='host ip')
parser.add_argument('-p', required=False, default=50124, type=int)
args = parser.parse_args()
port = args.p


# health check
url = "http://localhost:{}/health".format(port)

# simulate direct message
url = "http://localhost:{}/direct_message".format(port)

send_data = {
    "user_id": 50124,
    "user_name": "un1",
    "message_time": time.time(),
    "message_content": ",jrrp"
}
json_data = json.dumps(send_data)

header_dict = {'Content-Type': 'application/json'}

r = requests.post(url, headers=header_dict, data=json_data, timeout=20000)
print(r)
print(r.json())


# simulate group message
url = "http://localhost:{}/group_message".format(port)

send_data = {
    "user_id": 50124,
    "user_name": "un1",
    "message_time": time.time(),
    "message_content": ",jrrp"
}
json_data = json.dumps(send_data)

header_dict = {'Content-Type': 'application/json'}

r = requests.post(url, headers=header_dict, data=json_data, timeout=20000)
print(r)
print(r.json())