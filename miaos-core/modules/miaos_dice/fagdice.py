import random
import time
import sys

def isascii_py36(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())

if sys.version_info.minor < 7:
    isascii = isascii_py36
    
def get_random_int(minv, maxv, idx=0):
    rnd_state = random.getstate()
    random.seed(int(time.time() * 1000 + idx ** idx))
    result = random.randint(minv, maxv)
    random.setstate(rnd_state)
    return result

def rollnd6(num_d6=3, extra_dice=0, with_raw_result=False):
    
    raw_result = [get_random_int(1, 6, i) for i in range(num_d6 + abs(extra_dice))]
    raw_result.sort()
    rollsum = 0
    rolldes = ''
    if extra_dice > 0:
        rollsum = int(sum(raw_result[:num_d6]))
        rolldes = '+'.join([str(i) for i in raw_result[:num_d6]]) + \
            ' (drop {})'.format('、'.join([str(i) for i in raw_result[num_d6:]])) + '='
    elif extra_dice < 0:
        rollsum = int(sum(raw_result[-1*num_d6:]))
        rolldes = '+'.join([str(i) for i in raw_result[-1*num_d6:]]) + \
            ' (drop {})'.format('、'.join([str(i) for i in raw_result[:-1*num_d6]])) + '='
    else:
        rollsum = int(sum(raw_result))
        rolldes = '+'.join([str(i) for i in raw_result]) + '='
    
    if with_raw_result:
        return rollsum, rolldes
    else:
        return rollsum

def fag_check(o, description='', extra_dice=0):
    if o > 20:
        o = 20
    if o < 0:
        o = 0
    roll, rolldes = rollnd6(3, extra_dice=extra_dice, with_raw_result=True)
    success_degree = int(max(o - roll, 0))
    obj_str = '3D6'
    if   extra_dice > 0:
        obj_str = '3D6 ({} 小数骰)'.format(extra_dice)
    elif extra_dice < 0:
        obj_str = '3D6 ({} 大数骰)'.format(-1 * extra_dice)
    if roll <= 4:
        result = '投掷 {}: {} ≤ {}: \n投掷结果为 {} {} \n 重大成功！成功度为{}'.format(description, obj_str, o, rolldes, roll, 15)
    elif roll == 5:
        result = '投掷 {}: {} ≤ {}: \n投掷结果为 {} {} \n 成功！成功度为{}'.format(description, obj_str, o, rolldes, roll, success_degree)
    elif roll == 16:
        result = '投掷 {}: {} ≤ {}: \n投掷结果为 {} {} \n 成功！'.format(description, obj_str, o, rolldes, roll)
    elif roll >= 17:
        result = '投掷 {}: {} ≤ {}: \n投掷结果为 {} {} \n 重大失败！'.format(description, obj_str, o, rolldes, roll)
    elif roll <= o:
        result = '投掷 {}: {} ≤ {}: \n投掷结果为 {} {} \n 成功！成功度为{}'.format(description, obj_str, o, rolldes, roll, success_degree)
    else:
        result = '投掷 {}: {} ≤ {}: \n投掷结果为 {} {} \n 失败！'.format(description, obj_str, o, rolldes, roll)
    return result
        
def roll3d6(description=''):
    rolls = [get_random_int(1, 6) for i in range(3)]
    rollstr = '+'.join([str(i) for i in rolls])
    result = '投掷 {}: 3D6 = {} = {} '.format(description, rollstr, sum(rolls))
    return result

def rolld100(o, description=''):
    roll = get_random_int(1, 100)

def roll_dice(cmd):
    result = dice_resolver(cmd, True)
    if result is None:
        return
    else:
        return '投掷 {} 的结果为 {}'.format(cmd, result)  
    

def roll_damage(db, description=''):
    basic_damage = rollnd6(2)
    bd_str = '基础伤害 2D6 = {}\n'.format(basic_damage)
    db_str = ''
    bonus_damage = 0
    if db >= 3:
        db_roll = rollnd6(3)
        bonus_damage = int(max(0, db - db_roll))
        db_str = '伤害加深 目标： {} 投掷结果： {} 伤害数值 {}\n'.format(db, db_roll, bonus_damage)
    final_damage = basic_damage + bonus_damage
    result = '投掷 {}: 伤害检定 \n'.format(description) + bd_str +db_str + '最终伤害： {} + {} = {}'.format(basic_damage, bonus_damage, final_damage)
    return result
    
def roll_damage_npc(db, description=''):
    basic_damage = rollnd6(1)
    bd_str = '基础伤害 1D6 = {}\n'.format(basic_damage)
    db_str = ''
    bonus_damage = 0
    if db >= 3:
        db_roll = rollnd6(3)
        bonus_damage = int(max(0, db - db_roll))
        db_str = '伤害加深 目标： {} 投掷结果： {} 伤害数值 {}\n'.format(db, db_roll, bonus_damage)
    final_damage = basic_damage + bonus_damage
    result = '投掷 {}: 伤害检定 \n'.format(description) + bd_str +db_str + '最终伤害： {} + {} = {}'.format(basic_damage, bonus_damage, final_damage)
    return result

def roll_damage_custom(dmg_str, db, description=''):
    basic_damage = dice_resolver(dmg_str, result_only=True)
    if basic_damage is None:
        return
    bd_str = '基础伤害 {} = {}\n'.format(dmg_str, basic_damage)
    db_str = ''
    bonus_damage = 0
    if db >= 3:
        db_roll = rollnd6(3)
        bonus_damage = int(max(0, db - db_roll))
        db_str = '伤害加深 目标： {} 投掷结果： {} 伤害数值 {}\n'.format(db, db_roll, bonus_damage)
    final_damage = basic_damage + bonus_damage
    result = '投掷 {}: 伤害检定 \n'.format(description) + bd_str +db_str + '最终伤害： {} + {} = {}'.format(basic_damage, bonus_damage, final_damage)
    return result


def dice_resolver(dice_str, result_only=False):
    # if not isascii(dice_str):
    #     return None
    dice_str = dice_str.strip().lower()
    dices = []
    dice = ''
    chars_ignored = ''
    for char in dice_str:
        if char in ['+', '-']:
            dices.append(dice)
            dices.append(char)
            dice = ''
            continue

        if char.isdigit() or char == 'd':
            dice += char
            continue

        chars_ignored += char

    dices.append(dice)

    result = 0
    roll = 0
    rolls = []
    for i in range(len(dices)):
        item = dices[-1 * (i+1)]
        if item == '':
            continue
        if item == '+':
            result += roll
            roll = 0
            continue
        if item == '-':
            result -= roll
            roll = 0
            continue
        
        if 'd' in item:
            num = item.split('d')[0]
            dice_type = item.split('d')[-1]
            if not num.isdigit():
                num = '1'
            if not dice_type.isdigit():
                dice_type = '6'
            num = int(num)
            dice_type = int(dice_type)
            roll = sum([get_random_int(1, dice_type) for j in range(num)])
            rolls.append(roll)
            continue
        else:
            roll = int(item)
            rolls.append(roll)
    rolls.reverse()
    result += roll
    # if chars_ignored:
    #     print('ignore chars:' + chars_ignored)
    if result_only:
        return result
    else:
        return [result, rolls, chars_ignored]