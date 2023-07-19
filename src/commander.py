import os
import signal
import subprocess
import atexit
import logging

logging.basicConfig(level=logging.DEBUG)

workers_items = [
    {"command": ['python3', 'worker.py'], "arguments": ["test1"]},
    {"command": ['python3', 'worker.py'], "arguments": ["test2"]}
]

# Create a list to hold child process objects
workers = []


def start_worker_process(command, arguments):
    global workers
    full_command = command + [str(os.getpid())] + arguments
    worker = subprocess.Popen(full_command)
    workers.append(worker)
    logging.debug(f'Worker {command}({arguments}) #{worker.pid} started...')


def stop_worker_process(worker):
    worker.terminate()


def stop_workers(workers):
    for worker in workers:
        stop_worker_process(worker)
        logging.debug(f'Worker #{worker.pid} stopped...')


def run_workers(workers_items):
    for worker in workers_items:
        start_worker_process(worker['command'], worker['arguments'])

    # Register the signal handler for SIGTERM
    signal.signal(signal.SIGTERM, lambda signum, frame: stop_workers(workers))

    # Wait for child processes to complete
    for worker in workers:
        worker.wait()


def shutdown():
    stop_workers(workers)


def restart_workers():
    stop_workers(workers)
    run_workers(workers_items)


def run():
    atexit.register(shutdown)
    run_workers(workers_items)


if __name__ == '__main__':
    run()
