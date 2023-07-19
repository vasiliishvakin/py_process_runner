# Parent-Child Process Executor

This repository contains a Python script to manage a group of child processes (workers) using the parent process.

## Requirements

- Python 3.x
- `psutil` library (install using `pip install psutil`)

## Usage

1. Clone the repository or copy the contents of the provided README.md to your project directory.

2. Create a `worker.py` file with the worker logic. This script will be executed by each child process.

3. Modify the workers_items list in main.py to specify the commands and arguments for your worker processes.

4. Run the commander.py script to start the parent process and the child workers.
