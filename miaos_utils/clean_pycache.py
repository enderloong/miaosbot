import os
from shutil import rmtree
import platform
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument('--remove_so', default=False, action='store_true')
args = parser.parse_args()

REMOVE_SO=args.remove_so

dirs_to_clean = [
    '__pycache__', 
    '.ipynb_checkpoints'
]

dirs_to_clean = tuple(dirs_to_clean)
exts_to_clean = ['.pyc',]
if REMOVE_SO:
    exts_to_clean.append('.so')

def clear(filepath):
    files = os.listdir(filepath)
    for fd in files:
        cur_path = os.path.join(filepath, fd)            
        if os.path.isdir(cur_path):
            if fd in dirs_to_clean:
                print("rm %s -rf" % cur_path)
                if platform.platform().startswith('Windows'):
                    rmtree(cur_path)
                else:
                    os.system("rm %s -rf" % cur_path)
            else:
                clear(cur_path)
    for fd in files:
        cur_path = os.path.join(filepath, fd)            
        if os.path.isfile(cur_path):
            if fd.endswith(tuple(exts_to_clean)):
                print('rm %s' % cur_path)
                os.remove(cur_path)

if __name__ == "__main__":
    clear(".")