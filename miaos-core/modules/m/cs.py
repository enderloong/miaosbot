import random
import time
import os.path as osp

def get_random_int(minv, maxv, idx=0):
    rnd_state = random.getstate()
    random.seed(int(time.time() * 1000 + idx ** idx))
    result = random.randint(minv, maxv)
    random.setstate(rnd_state)
    return result

def chisha(chisha_fpath=osp.join(osp.dirname(__file__), '..', '..', 'data', 'm', 'chisha.txt')):
    lines = ['我也不知道']
    if osp.exists(chisha_fpath):
        with open(chisha_fpath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
    return random.choice(lines)