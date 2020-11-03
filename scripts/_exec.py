import subprocess
import shlex
import signal
import sys

def exec(cmd: str, log: bool = False):
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, shell=True)
    signal.signal(signal.SIGINT, lambda sig, frame: _stop_process(process))
    encodings = ['utf-8', 'cp866']
    while True:
        line = process.stdout.readline()
        if not line:
            break
        if log:
            for e in encodings:
                try:
                    print(line.decode(e), end='')
                except UnicodeDecodeError:
                    pass
                else:
                    break 
