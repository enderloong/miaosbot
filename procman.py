import subprocess, sys, os
import argparse as ap
import time

parser = ap.ArgumentParser()
parser.add_argument('--sleep', type=int, default=3, help='Waiting time after restarting process, in case lock is not released')
args = parser.parse_args()

PROCMAN_RESTART_SLEEP = args.sleep
if os.environ.get('PROCMAN_RESTART_SLEEP', ''):
    try:
        PROCMAN_RESTART_SLEEP = int(os.environ.get('PROCMAN_RESTART_SLEEP', 0))
    except ValueError:
        PROCMAN_RESTART_SLEEP = args.sleep
        print('PROCMAN_RESTART_SLEEP must be int, use default value {}'.format(PROCMAN_RESTART_SLEEP))

WORK_DIR = '/home/azureuser/miaosbot/miaos-core/'
RUN_LIST = [
    "gunicorn server_restapi:app -c miaos_utils/gunicorn.conf.py",
    "python3 ../miaos-interface/kook-khl.py/bot_to_miaos.py"
]

def start_process(cmd):
    proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True, cwd=WORK_DIR)
    if proc.poll() is not None:
        if proc.returncode != 0:
            print("Process {} failed to start command : -{}- (return code {})".format(proc.pid, cmd, proc.returncode))
        else:
            print("Process {} finished with command {}, and will not be restarted.".format(proc.pid, cmd))
        return None
    return proc

def auto_restart(proc: subprocess.Popen, cmd):
    if proc.poll() is not None:
        print('Auto restart...')
        if proc.returncode == 0:
            print('process {} ended'.format(proc.pid))
        else:
            print('process {} exited with code {}'.format(proc.pid, proc.returncode))
        proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True, cwd=WORK_DIR)
    return proc

def run_process_manager():
    raw_proc_list = [(cmd, start_process(cmd)) for cmd in RUN_LIST]
    monitored_run, proc_list = [], []
    for raw_proc in raw_proc_list:
        if raw_proc[1] is not None:
            monitored_run.append(raw_proc[0])
            proc_list.append(raw_proc[1])
    while True:
        if len(proc_list) == 0:
            print("No processes to monitor")
            break
        for idx, proc in enumerate(proc_list):
            if proc.poll() is not None:
                proc_list[idx] = auto_restart(proc, monitored_run[idx])
                print("Restarted process with pid {}: -{}-".format(proc_list[idx].pid, monitored_run[idx]))
                print("Waiting for {} seconds...".format(PROCMAN_RESTART_SLEEP))
                time.sleep(PROCMAN_RESTART_SLEEP)

if __name__ == '__main__':
    run_process_manager()