import asyncio
import sys
import json
from cmd import Cmd
import argparse as ap
import time, datetime
import socketio
from collections import deque

'''
event list emitted by user:
- login: 登录
- logout: 登出
- enter room: 进入房间
- leave room: 离开房间
- roll: 投掷
- message: 向用户发送的私聊信息
'''

parser = ap.ArgumentParser()
parser.add_argument('--url', '-u', type=str, default='http://localhost:50124')
args = parser.parse_args()

# standard Python
sio = socketio.Client()

CLIENT_LOGS = []
def client_print(line):
    global CLIENT_LOGS
    print(line)
    CLIENT_LOGS.append(line)
    
LOGIN_DATA = deque()
@sio.on('login response')
def rcv_login_response(data):
    global LOGIN_DATA
    login_response = json.loads(data)
    LOGIN_DATA.append(login_response)
    
@sio.on('response')
def rcv_response(data):
    _response = json.loads(data)
    print(_response)

@sio.on('loginout broadcast')
def rcv_loginout_broadcast(data):
    loginout_broadcast = json.loads(data)
    client_print(loginout_broadcast['message'])
    
@sio.on('miaos broadcast')
def rcv_miaos_broadcast(data):
    message_broadcast = json.loads(data)
    client_print(message_broadcast['message'])
    
@sio.on('miaos response')
def rcv_miaos_response(data):
    message_broadcast = json.loads(data)
    client_print(message_broadcast['message'])
    
@sio.event
def connect():
    print("Connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("Disconnected!")

class MiaosClient(Cmd):
    """
    客户端
    """
    prompt = ''
    intro = '[Welcome] 喵沌老师聊天室\n' + '[Welcome] 输入help来获取帮助\n'

    def __init__(self, url, sio: socketio.Client):
        """
        构造
        """
        super().__init__()
        self.sio = sio
        self.__username = None
        self.__isLogin = False
        self.url = url
                

    def start(self):
        """
        启动客户端
        """
        self.sio.connect(url=self.url)
        self.cmdloop()
        
    async def _corou_wait_for_login(self, user_name):
        # 尝试接受数据
        global LOGIN_DATA
        time_start = time.time()
        while len(LOGIN_DATA) == 0:
            time.sleep(0.01)
            if time.time() - time_start > 5:
                client_print('连接丢失')
                break
        if len(LOGIN_DATA) > 0:
            login_response = LOGIN_DATA.popleft()
            if login_response.get('result_code', 20000):
                self.__username = user_name
                self.__isLogin = True
                client_print('[Client] 成功登录到聊天室')
            else:
                client_print('[Client] 无法登录到聊天室')

    def do_login(self, args):
        """
        登录聊天室
        :param args: 参数
        """
        user_name = args.split()[0]

        # 将昵称发送给服务器，获取用户id
        self.sio.emit('login', json.dumps({
            'user_name': user_name
        }).encode())
        asyncio.run(self._corou_wait_for_login(user_name))
        
    def do_enter(self, args):
        splited = args.split()
        room_name = splited[0] if len(splited) > 0 else ''
        room_pwd = ''
        if len(splited) > 1:
            room_pwd = splited[1]
        self.sio.emit('enter room', json.dumps({
            'room_name': room_name,
            'room_pwd': room_pwd
        }))
        
    def do_leave(self, args):
        splited = args.split()
        room_name = splited[0] if len(splited) > 0 else ''
        self.sio.emit('leave room', json.dumps({
            'room_name': room_name
        }))
        
    def do_whereami(self, args):
        self.sio.emit('query room')
            
    async def _corou_send_message(self, message):
        """
        发送消息线程
        :param message: 消息内容
        """
        if self.__isLogin:
            self.sio.emit('message', json.dumps({
                'message': message
            }).encode())
        else:
            print('未登录')
        
    def do_send(self, args):
        """
        发送消息
        :param args: 参数
        """
        message = args
        asyncio.run(self._corou_send_message(message))
        
    async def _corou_roll(self, message):
        """
        发送消息线程
        :param message: 消息内容
        """
        if self.__isLogin:
            self.sio.emit('roll', json.dumps({
                'message_time': time.time(),
                'message_content': message
            }).encode())
        else:
            print('未登录')
        
    def do_jrrp(self, args=''):
        asyncio.run(self._corou_roll('jrrp'))
        
    def do_rf(self, args=''):
        message = 'rf ' + args
        asyncio.run(self._corou_roll(message))
        
    def do_rfb(self, args=''):
        message = 'rfb ' + args
        asyncio.run(self._corou_roll(message))
        
    def do_ro(self, args=''):
        message = 'ro ' + args
        asyncio.run(self._corou_roll(message))
        
    def do_rd(self, args=''):
        message = 'rd ' + args
        asyncio.run(self._corou_roll(message))
        
    def do_rdc(self, args=''):
        message = 'rdc ' + args
        asyncio.run(self._corou_roll(message))
        
    def do_r(self, args=''):
        message = 'r ' + args
        asyncio.run(self._corou_roll(message))

    def do_logout(self, args=None):
        """
        登出
        :param args: 参数
        """
        global CLIENT_LOGS
        self.sio.emit('logout')
        self.__isLogin = False
        logpath = 'client-{}-{}.log'.format(self.__username, datetime.datetime.now().ctime().replace(' ', '_').replace(':', '_'))
        with open(logpath, 'w', encoding='utf-8', newline='\n') as f:
            f.writelines(CLIENT_LOGS)
            CLIENT_LOGS = []
            

    def do_help(self, arg):
        """
        帮助
        :param arg: 参数
        """
        command = arg.split(' ')[0]
        if command == '':
            print('[Help] login nickname - 登录到聊天室，nickname是你选择的昵称')
            print('[Help] send message - 发送消息，message是你输入的消息')
            print('[Help] logout - 退出聊天室')
        elif command == 'login':
            print('[Help] login nickname - 登录到聊天室，nickname是你选择的昵称')
        elif command == 'send':
            print('[Help] send message - 发送消息，message是你输入的消息')
        elif command == 'logout':
            print('[Help] logout - 退出聊天室')
        else:
            print('[Help] 没有查询到你想要了解的指令')

    def do_exit(self, args):
        self.do_logout()
        sys.exit(0)
    

if __name__ == '__main__':
    client = MiaosClient(url=args.url, sio=sio)
    client.start()