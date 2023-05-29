import sys

def deduplicate(fpath):
    lines = []
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = list(set(lines))
    with open(fpath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        deduplicate(sys.argv[1])