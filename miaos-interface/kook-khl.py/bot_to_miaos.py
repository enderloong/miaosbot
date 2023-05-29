import os
import json
import sys
import time

import requests
from khl import Bot, Message

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
if os.environ.get('MIAOS_KOOK_CONFIG_PATH', ''):
    config_path = os.environ.get('MIAOS_KOOK_CONFIG_PATH', '')
config = {}
if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

# init Bot
bot_token = config.get('token', '')
if os.environ.get('MIAOS_KOOK_TOKEN', ''):
    bot_token = os.environ.get('MIAOS_KOOK_TOKEN', '')

bot = Bot(token=bot_token, )

# ret_code:
# -1: 失败
#  0: 默认
#  1: 回复
#  2: 发送

# connect to miaos server
header_dict = {'Content-Type': 'application/json'}
def check_connection_to_miaos(urlbase='http://localhost:50124', verbose=False):
    try:
        r = requests.get(urlbase+'/health')
        if r.status_code == 200:
            if verbose:
                print('Connected to Miaos server')
            return True
    except:
        if verbose:
            print('Failed to connect to Miaos server')
        return False

def get_miaos_response(msg: Message, urlbase='http://localhost:50124'):
    ret_code, reply_msg, r_json = 0, '', {}
    if check_connection_to_miaos():
        try:
            send_data = {
                'user_id': msg.author.id,
                'user_name': msg.author.nickname,
                'message_time': time.time(),
                'message_content': msg.content.replace('，',','),
            }
            r = requests.post(url=urlbase+'/direct_message', data=json.dumps(send_data), headers=header_dict, timeout=30)
            if r.status_code == 200:
                r_json = r.json()
                ret_code = 1
            else:
                print('Failed to get miaos_response, status_code error: {}'.format(r.status_code))
        except Exception as e:
            print('Failed to get miaos_response: Error: {}; Traceback: {}'.format(e, sys.exc_info()[2]))
    else:
        print('Failed to connect to Miaos server!!!')
    if ret_code > 0:
        if r_json['result_code'] == 20000:
            if r_json['result_data']['output_type'] == 'string':
                reply_msg = r_json['result_data']['output_data']
        else:
            print('Miaos server returned an invalid response: {}'.format(r_json))
            ret_code = -1
    return ret_code, reply_msg, r_json

@bot.command(regex='^,.+')
async def miaos_command(msg: Message):
    ret_code, miaos_reply, miaos_response = get_miaos_response(msg)
    if ret_code == 1:
        await msg.reply(miaos_reply)
    if ret_code == 2:
        # print('guild:',msg.ctx.guild)
        # print('gate:',msg.ctx.gate)
        # print('channel:',msg.ctx.channel)
        await msg.ctx.channel.send(miaos_reply)
    
def check_miaos_bridge(urlbase='http://localhost:50829'):
    ret_code, reply_msg, r_json = 0, '', {}
    try:
        r = requests.get(url=urlbase+'/check', timeout=60)
        if r.status_code == 200:
            r_json = r.json()
            ret_code = 2
        else:
            print('Failed to get miaos_response, status_code error: {}'.format(r.status_code))
    except Exception as e:
        print('Failed to get miaos_response: Error: {}; Traceback: {}'.format(e, sys.exc_info()[2]))
    if ret_code > 0:
        if r_json['result_code'] == 20000:
            if r_json['result_data']['output_type'] == 'string':
                reply_msg = r_json['result_data']['output_data']
        else:
            print('Miaos bridge returned an invalid response: {}'.format(r_json))
            ret_code = -1
    return ret_code, reply_msg, r_json

# everything done, go ahead now!
if check_connection_to_miaos(verbose=True):
    print('Hello Miaos!')
    bot.run()
