
def get_help(helpargs):
    msg = ''
    if len(helpargs) == 1:
        msg = \
'''喵沌老师的帮助：
地图(,map): ,help map
每日运势(,jrrp): 查看每日运势。每天的数值都是固定的，相当于coc里的幸运属性，越大越好。
生成角色(,generate): ,help generate
骰子文档(,rf ,ro ,r ): ,help dice'''
    else:
        if helpargs[1] == 'map':
            msg = \
'''施工中
目前的map功能支持下述用法：
用法1 ,map create 1 2 3
创建map，token为‘1’， 高为2， 宽为3


'''
        if helpargs[1] == 'generate':
            msg = \
'''目前的generate角色功能仅支持生成御主
用法: ,generate master'''

        if helpargs[1] == 'dice':
            msg = \
'''目前的roll dice功能支持以下几种方式:
用法1. ,rf 12
示例结果: 
投掷 3D6 ≤ 12 结果为：[5 + 1 + 1 =] 7 
成功
成功度为 5

用法2. ,rf 12 魔力感知
示例结果: 
投掷 魔力感知: 3D6 ≤ 12 结果为：[3 + 5 + 1 =] 9 
成功
成功度为 3

用法3. ,ro 
示例结果: 
投掷结果为：4 + 6 + 5 = 15
说明: 仅投掷三枚6面骰

用法4. ,r 3d
示例结果: 
投掷 3d 结果为：8
说明: 缺省骰子面数时默认是6

用法5. ,r 3d4
示例结果:  
投掷 3d4 结果为：7
说明: 骰子面数可以设置

用法6. ,r 3d-1
示例结果: 
投掷 3d-2 结果为：11
说明: 缺省骰子面数时默认是6，后面可以为+或-，不要加空格

用法7. ,r 3d4+3
示例结果:  
投掷 3d4+3 结果为：7
说明: 可以在设置骰子面数时同时加减，不要加空格'''
    return msg