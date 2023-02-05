import os

gunicorn_port = int(os.environ.get("GUNICORN_PORT", "50124"))
bind = '0.0.0.0:{}'.format(gunicorn_port)

NUM_WORKERS = 0
if os.environ.get('GUNICORN_WORKERS', ''):
    NUM_WORKERS = os.environ.get('GUNICORN_WORKERS', '')
    if NUM_WORKERS.isnumeric():
        NUM_WORKERS = int(NUM_WORKERS)
    else:
        print('GUNICORN_WORKERS SHOULD BE INT, BUT GOT {}'.format(NUM_WORKERS))
        NUM_WORKERS = 1
        
workers = 1
if NUM_WORKERS > 0:
    workers = NUM_WORKERS