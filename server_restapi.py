
from flask import Flask, request, abort, session
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import sys
import json
import os
import time, datetime
from miaos_message_resolver import MiaosMessageResolver
from miaos_utils.status import *

app = Flask(__name__)

MIAOS_REQUEST_TIMEOUT = 300

message_resolver = MiaosMessageResolver()

socket_dict = {}

def preprocess_message_content(message_content):
    if message_content.startswith(','):
        return True, message_content[1:].split()
    else:
        return False, []

@app.route('/direct_message', methods=['POST', 'GET'])
def get_direct_message():
    return_dict = {'result_code':20000, 'message':'successful response', 'result_data':{}}
    notfinished = True
    try:
        _request_data = request.get_data()
        _request = json.loads(_request_data.decode('utf-8'))
        try:
            user_id = _request.get('user_id', '')
            user_name = _request.get('user_name', '')
            message_time = _request.get('message_time', '')
            message_content = _request.get('message_content', '')
        except Exception as e:
            raise MiaosParameterError(e, sys.exc_info()[2])
        is_miaos_message, cmd_and_args = preprocess_message_content(message_content)
        if not is_miaos_message:
            notfinished = False
            return_dict['message'] = 'not miaos message'
        if notfinished:
            cur_time = time.time()
            if cur_time - int(message_time) > MIAOS_REQUEST_TIMEOUT:
                return_dict = {
                    'result_code': 40800, 'message': 'This request is outdated. Miaos will ignore it',
                    'result_data': {
                        'message_time': message_time,
                        'miaos_time': cur_time,
                    }
                }
                notfinished = False
        if notfinished:
            result_data = message_resolver.resolve_direct_message(user_id, user_name, message_time, cmd_and_args)
            return_dict['result_data'] = result_data
    except MiaosErrorBase as e:
        return_dict = {'result_code':e.error_code, 'message': "Miaos Meet Error", 'result_data':{
            'error_message': e.error_msg,
            'error_type': str(e.raw_error),
            'traceback': sys.exc_info()[2]
        }}
    except Exception as e:
        return_dict = {'result_code':50000, 'message':'unknown error', 'result_data':{
            'error_message': 'Unknown Error',
            'error_type': str(e),
            'traceback': sys.exc_info()[2]
        }}
    return return_dict
    
@app.route('/group_message', methods=['POST', 'GET'])
def get_group_message():
    return_dict = {'result_code':20000, 'message':'successful response', 'result_data':{}}
    notfinished = True
    try:
        _request_data = request.get_data()
        _request = json.loads(_request_data.decode('utf-8'))
        try:
            user_id = _request.get('user_id', '')
            user_name = _request.get('user_name', '')
            group_id = _request.get('group_id', '')
            group_name = _request.get('group_name', '')
            message_time = _request.get('message_time', '')
            message_content = _request.get('message_content', '')
        except Exception as e:
            raise MiaosParameterError(e, sys.exc_info()[2])
        is_miaos_message, cmd_and_args = preprocess_message_content(message_content)
        if not is_miaos_message:
            notfinished = False
            return_dict['message'] = 'not miaos message'
        if notfinished:
            cur_time = time.time()
            if cur_time - int(message_time) > MIAOS_REQUEST_TIMEOUT:
                return_dict = {
                    'result_code': 40800, 'message': 'This request is outdated. Miaos will ignore it',
                    'result_data': {
                        'message_time': message_time,
                        'miaos_time': cur_time,
                    }
                }
                notfinished = False
        if notfinished:
            result_data = message_resolver.resolve_group_message(user_id, user_name,group_id,group_name,message_time, cmd_and_args)
            return_dict['result_data'] = result_data
    except MiaosErrorBase as e:
        return_dict = {'result_code':e.error_code, 'message': "Miaos Meet Error", 'result_data':{
            'error_message': e.error_msg,
            'error_type': str(e.raw_error),
            'traceback': sys.exc_info()[2]
        }}
    except Exception as e:
        return_dict = {'result_code':50000, 'message':'unknown error', 'result_data':{
            'error_message': 'Unknown Error',
            'error_type': str(e),
            'traceback': sys.exc_info()[2]
        }}
    return return_dict

@app.route('/health', methods=['GET'])
def get_healthy():
    return {'result_code':20090, 'message':'Hello Miaos SenSei!'}
        
if __name__ == '__main__':
    port = int(os.environ.get('MIAOS_PORT', 50124))
    app.run(host='0.0.0.0', port=port)