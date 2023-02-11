
import json
import sys
import time
import traceback as tb

import socketio
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from miaos_message_resolver import MiaosMessageResolver
from miaos_utils.status import *

sio = socketio.Server()
app = socketio.WSGIApp(sio)

MIAOS_REQUEST_TIMEOUT = 300

message_resolver = MiaosMessageResolver()

user_sid_dict = {}
sid_user_dict = {}
sid_room_dict = {}


'''
event list emitted by miaos:
- miaos response: 系统级别的信息
- miaos response login: 登录信息
- miaos forward: 信息的转发
- miaos broadcast: 服务端的公告
- miaos message: 向用户发送的私聊信息
'''

def response_login_required():
    _response = {
        'result_code':40300, 
        'result_message':'login required',
        'message': '需要登录'
    }
    sio.emit('miaos response', json.dumps(_response))
    
def response_room_required():
    _response = {
        'result_code':40301, 
        'result_message':'enter room required',
        'message': '需要进入房间'
    }
    sio.emit('miaos response', json.dumps(_response))
    
@sio.on('message')
def message(sid, data):
    message_data = json.loads(data)
    message = message_data.get('message', '')
    if sid in sid_user_dict:
        message_broadcast = {
            'result_code':20000, 
            'result_message':'successful response',
            'message': '[{}]:'.format(sid_user_dict[sid]) + message
        }
        print(message_broadcast['message'])
        if sid in sid_room_dict and len(sid_room_dict[sid]) > 0:
            for room in sid_room_dict[sid]:
                sio.emit('miaos broadcast', json.dumps(message_broadcast), room=room, broadcast=True)
        else:
            for room in sid_room_dict[sid]:
                sio.emit('miaos broadcast', json.dumps(message_broadcast), broadcast=True)
    else:
        response_login_required()

@sio.on('roll')
def miaos_roll(sid, data):
    return_dict = {'result_code':20000, 'result_message':'successful response', 'result_data':{}}
    notfinished = True
    try:
        _ws_message = json.loads(data)
        try:
            user_id = sid
            user_name = sid_user_dict[sid]
            group_id = _ws_message.get('group_id', '')
            group_name = _ws_message.get('group_name', '')
            message_time = _ws_message.get('message_time', time.time())
            message_content = _ws_message.get('message_content', '')
        except Exception as e:
            raise MiaosParameterError(e, sys.exc_info()[2])
        cmd_and_args = message_content.split()
        if notfinished:
            cur_time = time.time()
            if cur_time - int(message_time) > MIAOS_REQUEST_TIMEOUT:
                return_dict = {
                    'result_code': 40800, 'result_message': 'This request is outdated. Miaos will ignore it',
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
        return_dict = {'result_code':e.error_code, 'result_message': "Miaos Meet Error", 'result_data':{
            'error_message': e.error_msg,
            'error_type': str(e.raw_error),
            'traceback': tb.format_exc()
        }}
    except Exception as e:
        return_dict = {'result_code':50000, 'result_message':'unknown error', 'result_data':{
            'error_message': 'Unknown Error',
            'error_type': str(e),
            'traceback': tb.format_exc()
        }}
    if return_dict['result_code'] == 20000:
        if return_dict['result_data']['including_atauthor']:
            return_message = return_dict['result_data']['output_data'].replace(',m@author/m,',
                '@{} '.format(sid_user_dict[sid]))
        
            roll_broadcast = {
                'result_code':20000, 
                'result_message':'successful response',
                'message': '[miaos]:' + return_message
            } 
            sio.emit('miaos broadcast', json.dumps(roll_broadcast), broadcast=True)
        else:
            roll_broadcast = {
                'result_code':20000, 
                'result_message':'successful response',
                'message': '[miaos]:' + return_dict['result_data']['output_data']
            } 
            sio.emit('miaos broadcast', json.dumps(roll_broadcast), broadcast=True)
    else:
        print(return_dict)
        roll_broadcast = {
            'result_code': 40000, 
            'result_message':'fail to resolve',
            'message': '投掷语法错误'
        } 
        sio.emit('miaos response', json.dumps(roll_broadcast))

@sio.on('login')
def login(sid, data):
    return_dict = {
        'result_code': 40100,
        'result_message': 'Login Failed',
        'result_data': {}
    }
    notfinished = True
    login_data = json.loads(data)
    user_name = login_data.get('user_name', '')
    if len(user_name) == 0:
        return_dict['result_code'] = 40101
        return_dict['result_message'] = 'No user_name received'
        sio.emit('miaos response', json.dumps(return_dict))
        notfinished = False
    if notfinished:
        user_sid_dict[user_name] = sid
        sid_user_dict[sid] = user_name
        sid_room_dict[sid] = []
        return_dict['result_code'] = 10000
        return_dict['result_message'] = 'Login Success'
        sio.emit('login response', json.dumps(return_dict))
        loginout_broadcast = {
            'result_code': 20000,
            'result_message': 'login broadcast',
            'message': '[{}] 进入了聊天室'.format(user_name)
        }
        print(loginout_broadcast['message'])
        sio.emit('miaos broadcast', json.dumps(loginout_broadcast), room='', broadcast=True, skip_sid=sid)
        notfinished = False
        
@sio.on('enter room')
def enter_room(sid, data):
    message_data = json.loads(data)
    room_name = message_data.get('room_name', '')
    if sid in sid_user_dict:
        user_name = sid_user_dict[sid]
        if room_name not in sid_room_dict[sid]:
            sid_room_dict[sid].append(room_name)
            sio.enter_room(sid, room_name)
            room_message = {
                'result_code':20000, 
                'result_message':'successful response',
                'message': '[{}] 进入了房间 {}'.format(user_name, room_name)
            }
            sio.emit('miaos broadcast', json.dumps(room_message), room=room_name, broadcast=True)
        else:
            room_message = {
                'result_code':20000, 
                'result_message':'successful response',
                'message': '您已在房间中'
            }
            sio.emit('miaos response', json.dumps(room_message))
    else:
        response_login_required()

@sio.on('leave room')
def leave_room(sid, data):
    message_data = json.loads(data)
    room_name = message_data.get('room_name', '')
    if sid in sid_user_dict:
        user_name = sid_user_dict[sid]
        if room_name in sid_room_dict[sid]:
            sid_room_dict[sid] = [i for i in sid_room_dict[sid] if i != room_name]
            sio.leave_room(sid, room_name)
            room_message = {
                'result_code':20000, 
                'result_message':'successful response',
                'message': '{} 离开了了房间 {}'.format(user_name, room_name)
            }
            sio.emit('miaos broadcast', json.dumps(room_message), room=room_name, broadcast=True)
        else:
            room_message = {
                'result_code':20000, 
                'result_message':'successful response',
                'message': '您不在房间中'
            }
            sio.emit('miaos response', json.dumps(room_message))
    else:
        response_login_required()
        
@sio.on('query room')
def query_room(sid):
    if sid in sid_user_dict:
        room_response = {
            'result_code':20000, 
            'result_message':'successful response',
            'message': '当前的位置: '
        }
        if sid in sid_room_dict:
            if len(sid_room_dict[sid]) > 0:
                room_response['message'] += ','.join(sid_room_dict[sid])
            else:
                room_response['message'] += '大厅'
        else:
            room_response['message'] += '大厅'
        sio.emit('miaos response', json.dumps(room_response), broadcast=False)
    else:
        response_login_required()
        
@sio.on('logout')
def login(sid):
    if sid in sid_user_dict:
        user_name = sid_user_dict[sid]
        del sid_user_dict[sid], user_sid_dict[user_name]
        if sid in sid_room_dict:
            room_names = sid_room_dict[sid]
            del sid_room_dict[sid]
            for room_name in room_names:
                loginout_broadcast = {
                    'message': '{} 离开了房间 {}'.format(user_name, room_name)
                }
                sio.emit('miaos broadcast', json.dumps(loginout_broadcast), room=room_name, broadcast=True, skip_sid=sid)
        else:
            loginout_broadcast = {
                'message': '[{}] 离开了聊天室'.format(user_name)
            }
            print(loginout_broadcast['message'])
            sio.emit('miaos broadcast', json.dumps(loginout_broadcast), broadcast=True, skip_sid=sid)

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    if sid in sid_user_dict:
        user_name = sid_user_dict[sid]
        del sid_user_dict[sid], user_sid_dict[user_name]
        loginout_broadcast = {
            'result_message': '[{}] 断开了连接'.format(user_name)
        }
        print(loginout_broadcast['result_message'])
        sio.emit('miaos broadcast', json.dumps(loginout_broadcast), broadcast=True, skip_sid=sid)
    else:
        print('disconnected: ', sid)

if __name__ == '__main__':
    WSGIServer(('', 50124), app, handler_class=WebSocketHandler).serve_forever()
