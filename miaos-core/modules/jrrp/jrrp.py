import random
import datetime

def convert_data_to_seed(data):
    datastr = str(repr(data))
    dataseed = int.from_bytes(datastr.encode('utf-8'), byteorder='big')
    return dataseed

def getjrrp(user):
    userseed = convert_data_to_seed(user)
    today = datetime.date.today().ctime()
    dateseed = convert_data_to_seed(today)
    random.seed(userseed)
    userrnd = random.randint(0, 65535)
    random.seed(dateseed)
    daternd = random.randint(0, 65536)
    jrrpseed = userrnd * 65536 + daternd
    random.seed(jrrpseed)
    jrrp = random.randint(1, 100)
    result = '今日的运势指数为 {} !'.format(jrrp)
    return result
