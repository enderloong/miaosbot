import random
import time
import os.path as osp
from datetime import date

def get_random_int(minv, maxv, idx=0):
    rnd_state = random.getstate()
    random.seed(int(time.time() * 1000 + idx ** idx))
    result = random.randint(minv, maxv)
    random.setstate(rnd_state)
    return result

def chisha(chisha_fpath=osp.join(osp.dirname(__file__), '..', '..', 'data', 'm', 'chisha.txt')):
    lines = ['我也不知道']
    if date.today().weekday() == 0:
        if random.random() < 0.2:
            chisha_weekday_fpath = osp.join(osp.split(chisha_fpath)[0], 'chisha_monday.txt')
            if osp.exists(chisha_weekday_fpath):
                with open(chisha_fpath, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f.readlines()]
            else:
                lines = ['麦当劳']
    if date.today().weekday() == 3:
        if random.random() < 0.5:
            chisha_weekday_fpath = osp.join(osp.split(chisha_fpath)[0], 'chisha_thursday.txt')
            if osp.exists(chisha_weekday_fpath):
                with open(chisha_fpath, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f.readlines()]
            else:
                lines = ['肯德基']
            return random.choice(lines)
    if osp.exists(chisha_fpath):
        with open(chisha_fpath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
    return random.choice(lines)