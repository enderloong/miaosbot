from random import randint, seed
import datetime
from time import time
import json
import os
from os import path

cache_map_dir = path.join(path.dirname(__file__), '..', '..', 'data', 'temp', 'trpg_maps')

if not path.exists(cache_map_dir):
    os.mkdir(cache_map_dir)

TRPG_MAPS = {
    '0':{
        'height':10,
        'width':10,
        'points':[]
    }
}

TRPG_MAP = {
    'height':10,
    'width':10,
    'points':[]
}

def create_map(token, height=10, width=10):
    width = 10 if width > 10 else int(width)
    width = 1 if width < 1 else int(width)
    height = 36 if width > 36 else int(height)
    height = 1 if height < 1 else int(height)
    mapdata = {
        'height':height,
        'width':width,
        'points':{}
    }
    save_map(mapdata, token)

def reset_map(token='0'):
    global TRPG_MAPS
    TRPG_MAPS[token] = {
        'height':10,
        'width':10,
        'points':{}
    }

def show_map(token='0'):
    has_map, map_to_show = load_map(token)
    msg = ''
    if has_map:
        pts = {}
        for i in map_to_show['points'].keys():
            x, y = map_to_show['points'][i]
            pts[str(x)+'-'+str(y)] = i
        xords = ['一','二','三','四','五','六','七','八','九','十']
        msg += '00|'
        for i in range(map_to_show['width']):
            msg +=  xords[i] + '|'
        msg += '\n'
        for i in range(map_to_show['height']):
            msg += '{:0>2d}'.format(i+1)
            for j in range(map_to_show['width']):
                ordkey = str(j+1)+'-'+str(i+1)
                if ordkey in pts.keys():
                    msg += '|' + pts[ordkey]
                else:
                    msg += '|口'
            msg += '|\n'
        return msg
    else:
        return '没有地图:' + token

def map_set_pt(token, pt='', xord=0, yord=0):
    has_map, map_to_set = load_map(token)
    msg = ''
    if not (isinstance(xord, int) and isinstance(yord, int)):
        return '地图设置失败'
    if xord < 1 or yord < 1:
        return '座标越界'
    if has_map:
        map_to_set['points'][pt] = (xord, yord)
        save_map(mapdata=map_to_set, token=token)
        msg = '设置地图 {} 坐标 ({}, {}) 为 {}'.format(token, xord, yord, pt)
        return msg
    else:
        return '没有地图:' + token

def map_remove_pt(token, pt=''):
    has_map, map_to_set = load_map(token)
    msg = ''
    if has_map:
        global TRPG_MAPS
        map_to_set['points'].pop(pt, None)
        TRPG_MAPS[token]['points'].pop(pt, None)
        save_map(map_to_set, token)
        msg = '清除地图 {} 元件：{}'.format(token, pt)
        return msg
    else:
        return '没有地图:' + token

def save_map(mapdata, token='0'):
    mappath = path.join(cache_map_dir, token+'.json')
    with open(mappath, 'w') as mapfile:
        json.dump(mapdata, mapfile)

def load_map(token='0'):
    mappath = path.join(cache_map_dir, token+'.json')
    
    if path.exists(mappath):
        with open(mappath, 'r') as mapfile:
            mapdata = json.load(mapfile)
        return [True, mapdata]
    return [False, None]

def delete_map(token):
    msg = ''
    if path.exists(path.join(cache_map_dir, token+'.json')):
        os.remove(path.join(cache_map_dir, token+'.json'))
        msg = '删除地图：' + token
    else:
        msg = '没有地图：' + token
    return msg

def show_map_tokens():
    global TRPG_MAPS
    msg = '|'.join([str(i) for i in TRPG_MAPS.keys() if i != '0'])
    return msg

def load_all_maps():
    global TRPG_MAPS
    for json_name in os.listdir(cache_map_dir):
        mappath = path.join(cache_map_dir, json_name)
        token = os.path.splitext(json_name)[0]
        with open(mappath, 'r') as mapfile:
            mapdate = json.load(mapfile)
            TRPG_MAPS[token] = mapdate
    msg = '已加载地图:' + show_map_tokens()
    return msg

def map_funcs(map_cmds_and_args):
    msg = ''
    if len(map_cmds_and_args) < 1:
        msg = '请输入map help查看帮助'
    if map_cmds_and_args[0] == 'create' and len(map_cmds_and_args[1]) > 0:
        if len(map_cmds_and_args) > 3:
            h, w = int(map_cmds_and_args[2]), int(map_cmds_and_args[3]) 
            create_map(token=map_cmds_and_args[1], height=h, width=w)
        else:
            create_map(token=map_cmds_and_args[1])
        msg = '创建地图：' + map_cmds_and_args[1]
    
    if map_cmds_and_args[0] == 'set' and len(map_cmds_and_args[1]) > 0:
        # map set token pt x y
        if len(map_cmds_and_args) > 4:
            x, y = int(map_cmds_and_args[3]), int(map_cmds_and_args[4])
            msg = map_set_pt(token=map_cmds_and_args[1], pt=map_cmds_and_args[2], xord=x, yord=y)
        else:
            msg = '设置坐标失败'

    if map_cmds_and_args[0] == 'rm' and len(map_cmds_and_args[1]) > 0:
        if len(map_cmds_and_args) > 2:
            msg = map_remove_pt(token=map_cmds_and_args[1], pt=map_cmds_and_args[2])
        else:
            msg = '请输入地图名称和坐标'

    if map_cmds_and_args[0] == 'show' and len(map_cmds_and_args[1]) > 0:
        msg = show_map(token=map_cmds_and_args[1])

    if map_cmds_and_args[0] == 'delete' and len(map_cmds_and_args[1]) > 0:
        msg = delete_map(token=map_cmds_and_args[1])

    #TODO(lyl): add admin permission
    if map_cmds_and_args[0] == 'all':
        msg = '目前已有的地图：' + show_map_tokens()

    if map_cmds_and_args[0] == 'loadall':
        msg = load_all_maps()
    
    if map_cmds_and_args[0] == 'load' and len(map_cmds_and_args[1]) > 0:
        msg = load_map(token=map_cmds_and_args[1])
    return msg


def auto_gen_master(num=1):
    msg = ''
    for i in range(num):
        msg += '  御主属性' 
        cons1 = int(sum([randint(1, 6) for j in range(3)])) 
        cons2 = int(sum([randint(1, 6) for j in range(3)])) 
        msg += '  体质：' + str(cons1) + ' | ' + str(cons2)
        mana1 = int(sum([randint(1, 6) for j in range(3)])) 
        mana2 = int(sum([randint(1, 6) for j in range(3)])) 
        msg += '  资质：' + str(mana1) + ' | ' + str(mana1)
        tech1 = int(sum([randint(1, 6) for j in range(3)])) 
        tech2 = int(sum([randint(1, 6) for j in range(3)])) 
        msg += '  技巧：' + str(tech1) + ' | ' + str(tech2)
        soci1 = int(sum([randint(1, 6) for j in range(3)])) 
        soci2 = int(sum([randint(1, 6) for j in range(3)])) 
        msg += '  社会：' + str(soci1) + ' | ' + str(soci2)
        if num > i + 1:
            msg += '\n'
    return msg

def auto_gen_character(genargs):
    msg = ''
    if genargs[0] == 'master':
        if len(genargs) > 1:
            num = int(genargs[1])
            num = 1 if num < 1 else num
            num = 5 if num > 5 else num
            msg = auto_gen_master(num)
        else:
            msg = auto_gen_master()
    
    # if genargs[0] == 'servant':
    #     if len(genargs) > 1:
    #         pass
    #     else:
    #         pass

    return msg
