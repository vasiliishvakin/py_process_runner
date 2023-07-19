import os
import sys
import time
import multiprocessing
import logging
import psutil
import signal
import atexit

parent_pid = int(sys.argv[1])
arguments = sys.argv[1:]

logging.basicConfig(level=logging.DEBUG)
parent_watcher = None


def check_parent_process(parent_pid, my_pid):
    while True:
        try:
            parent_process = psutil.Process(parent_pid)
            if parent_process.status() == psutil.STATUS_ZOMBIE:
                print(f'Parent process has terminated. Exiting...')
                os.kill(my_pid, signal.SIGTERM)
                sys.exit(0)
        except psutil.NoSuchProcess:
            print(f'Parent process is no longer running. Exiting...')
            os.kill(my_pid, signal.SIGTERM)
            sys.exit(0)
        time.sleep(15)


def start_parent_watcher():
    global parent_watcher
    my_pid = os.getpid()
    parent_watcher = multiprocessing.Process(
        target=check_parent_process, args=(parent_pid, my_pid))
    parent_watcher.start()


def run():
    while True:
        time.sleep(30)
        logging.debug(
            f'Worker {os.getppid()}/{os.getpid()} with arguments ({" ".join(arguments)}) is running...')


def shutdown():
    global parentWatcher
    if parentWatcher is not None and parentWatcher.is_alive():
        parentWatcher.terminate()


if __name__ == '__main__':
    start_parent_watcher()
    atexit.register(shutdown)
    run()
