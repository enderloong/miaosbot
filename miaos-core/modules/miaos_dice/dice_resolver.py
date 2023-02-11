
from random import randint


def dice_resolver(dice_str):
    # if not dice_str.isascii():
    #     return 'not ascii str!'
    
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
            roll = sum([randint(1, dice_type) for j in range(num)])
            rolls.append(roll)
            continue
        else:
            roll = int(item)
            rolls.append(roll)
    rolls.reverse()
    print(rolls)
    result += roll
    if chars_ignored:
        print('ignore chars:' + chars_ignored)
    return result


if __name__ == "__main__":
    roll1 = '1d'
    roll2 = '1'
    roll3 = 'd'
    roll4 = 'D6'
    roll5 = '投'
    roll6 = '1d6'

    rolls = [roll1,roll2, roll3, roll4, roll5]
    rolls = [
        '1d6',
        'a+1',
        '1+1',
        'a1+1',
        '1d+1',
        '1d+2d',
        'd+3',
        '2d+3d6',
    ]
    for roll in rolls:
        print('processing:' + roll)
        print('result:', dice_resolver(roll))