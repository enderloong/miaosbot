import os,sys
from io import BytesIO

import requests
sys.path.insert(0, os.path.dirname(__file__))
import modules.miaos_dice.fagdice as fd
from modules.jrrp.jrrp import getjrrp
import data.pers.hj_gif as hj_gif
import modules.miaos_help as miaos_help
import modules.trpgmap.trpgmap as trpgmap
from modules.m import chisha
class MiaosMessageResolver(object):
    
    atauthor = ',m@author/m,'

    def __init__(self):
        pass

    def resolve_direct_message(self, user_id, user_name, message_time, cmd_and_args):
        return_data = {
            'output_type': 'string',
            'including_atauthor': False,
            'output_data': ''
        }
        
        if cmd_and_args[0] == 'jrrp':
            return_data['output_data'] = getjrrp(user_id)
            return return_data

        if cmd_and_args[0] == 'rf': # roll fag check
            if len(cmd_and_args) in [2, 3]:
                if not cmd_and_args[1].isdigit():
                    return
                obj = int(cmd_and_args[1])
                if len(cmd_and_args) == 3:
                    roll_str = fd.fag_check(obj, cmd_and_args[2])
                else:
                    roll_str = fd.fag_check(obj)
                return_data['output_data'] = roll_str
                return return_data
            
        if cmd_and_args[0] == 'rfb': # roll fag check with bonus
            if len(cmd_and_args) in [3, 4]:
                if not cmd_and_args[1].isdigit():
                    return
                obj = int(cmd_and_args[1])
                extra_dice = int(cmd_and_args[2])
                if len(cmd_and_args) == 4:
                    roll_str = fd.fag_check(obj, cmd_and_args[3], extra_dice)
                else:
                    roll_str = fd.fag_check(obj, extra_dice=extra_dice)
                return_data['output_data'] = roll_str
                return return_data
        
        if cmd_and_args[0] == 'ro': # roll only
            if len(cmd_and_args) in [1, 2]:
                if len(cmd_and_args) == 2:
                    roll_str = fd.roll3d6(cmd_and_args[1])
                else:
                    roll_str = fd.roll3d6()
                return_data['output_data'] = roll_str
                return return_data

        if cmd_and_args[0] == 'rd': # roll damage
            if len(cmd_and_args) in [2, 3]:
                if not cmd_and_args[1].isdigit():
                    return
                db_val = int(cmd_and_args[1])
                if len(cmd_and_args) == 2:
                    dmg_str = fd.roll_damage(db_val)
                else:
                    dmg_str = fd.roll_damage(db_val, cmd_and_args[2])
                return_data['output_data'] = dmg_str
                return return_data

        if cmd_and_args[0] == 'rdc': # roll damage custom
            if len(cmd_and_args) in [3, 4]:
                if not cmd_and_args[2].isdigit():
                    return
                db_val = int(cmd_and_args[2])
                if len(cmd_and_args) == 3:
                    dmg_str = fd.roll_damage_custom(cmd_and_args[1], db_val)
                else:
                    dmg_str = fd.roll_damage_custom(cmd_and_args[1], db_val, cmd_and_args[3])
                return_data['output_data'] = dmg_str
                return return_data

        if cmd_and_args[0] == 'r': # roll normal dice
            if len(cmd_and_args) in [2, 3]:
                result = fd.roll_dice(cmd_and_args[1])
                if result == '':
                    return
                if len(cmd_and_args) == 3:
                    return_data['output_data'] = '{} '.format(cmd_and_args[2]) + result
                else:
                    return_data['output_data'] = result
                return return_data

        if cmd_and_args[0] == 'm':
            if len(cmd_and_args) > 1:
                if cmd_and_args[1] in ['吃啥', '今天吃啥', '中午吃啥', '晚上吃啥', '等会吃啥']:
                    return_data['output_data'] = chisha()
                return return_data

        if cmd_and_args[0] == 'map':
            mapargs = cmd_and_args[1:]
            return_data['output_data'] = {
                'map': trpgmap.map_funcs(mapargs)
            }
            return_data['output_type'] = 'map'
            return return_data

        if cmd_and_args[0] == 'gif':
            gif_name = cmd_and_args[1]
            gif_url = hj_gif.gif_database.get(gif_name)
            if gif_url is not None:
                gif_bytes = requests.get(gif_url, allow_redirects=True).content
                return_data['output_data'] = BytesIO(gif_bytes)
                return_data['output_type'] = 'gif'
                return return_data

        if cmd_and_args[0] == 'help':
            return_data['output_data'] = miaos_help.get_help(cmd_and_args)
            return return_data
        return return_data

    def resolve_group_message(self, user_id, user_name, 
                              group_id, group_name,
                              message_time, cmd_and_args):
        return_data = {
            'output_type': 'string',
            'including_atauthor': False,
            'output_data': ''
        }
        direct_return_data = self.resolve_direct_message(user_id, user_name, message_time, cmd_and_args)
        
        if cmd_and_args[0] == 'jrrp':
            return_data['including_atauthor'] = True
            return_data['output_data'] = self.atauthor + direct_return_data['output_data']
            return return_data

        if cmd_and_args[0] == 'rf':
            return_data['including_atauthor'] = True
            return_data['output_data'] = self.atauthor + direct_return_data['output_data']
            return return_data
        
        if cmd_and_args[0] == 'ro':
            return_data['including_atauthor'] = True
            return_data['output_data'] = self.atauthor + direct_return_data['output_data']
            return return_data

        if cmd_and_args[0] == 'rd':
            return_data['including_atauthor'] = True
            return_data['output_data'] = self.atauthor + direct_return_data['output_data']
            return return_data

        if cmd_and_args[0] == 'rdc':
            return_data['including_atauthor'] = True
            return_data['output_data'] = self.atauthor + direct_return_data['output_data']
            return return_data

        if cmd_and_args[0] == 'r':
            return_data['including_atauthor'] = True
            return_data['output_data'] = self.atauthor + direct_return_data['output_data']
            return return_data
        
        if cmd_and_args[0] == 'm':
            return_data['output_data'] = direct_return_data['output_data']
            return return_data

        if cmd_and_args[0] == 'map':
            return_data['output_data'] = direct_return_data['output_data']
            return return_data

        if cmd_and_args[0] == 'gif':
            return_data['output_data'] = direct_return_data['output_data']
            return return_data

        if cmd_and_args[0] == 'help':
            return_data['output_data'] = direct_return_data['output_data']
            return return_data
        return return_data
