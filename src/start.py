import sys
import time
from pathlib import Path
from queue import Queue
from threading import Thread, Event
from typing import List

PROJECT_DIR = str(Path(__file__).resolve().parent.parent)
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from src.message import Message
from src.producer import gen_msg_queue
from src.sender import Sender
from src.monitor import Monitor


def run_simulation(
        num_msgs: int,
        num_senders: int,
        mean_proc_time: float,
        max_deviation: float,
        failure_rate: float) -> None:

    print(f'Generating {num_msgs} messages...')
    input_q = gen_msg_queue(num_msgs)

    output_q: Queue[Message] = Queue()
    failure_q: Queue[Message] = Queue()
    stop_event: Event = Event()

    print(f'Starting {num_senders} senders...')
    sender_args = (input_q, output_q, failure_q, stop_event, mean_proc_time, max_deviation, failure_rate)
    sender_threads: List[Thread] = [Thread(target=Sender, args=sender_args) for _ in range(num_senders)]
    for thread in sender_threads:
        thread.start()

    print('Starting Monitor...')
    monitor = Monitor(output_q, failure_q, time.time(), num_senders)

    while not input_q.empty():
        time.sleep(1)
        print(f'Monitor status: {monitor.status().__dict__}')  # TODO make into static display
    print(f'Monitor status: {monitor.status().__dict__}')

    print('All messages processed. Stopping senders...')
    stop_event.set()
    for thread in sender_threads:
        thread.join()


def _process_args() -> tuple:
    num_messages = _parse_int_arg(sys.argv[1], 'num_messages', req_positive=True)
    num_senders = _parse_int_arg(sys.argv[2], 'num_senders', req_positive=True)
    mean_processing_time = _parse_float_arg(sys.argv[3], 'mean_processing_time', req_non_negative=True)
    max_deviation = _parse_float_arg(sys.argv[4], 'max_deviation', req_non_negative=True)
    failure_rate = _parse_float_arg(sys.argv[5], 'failure_rate', req_non_negative=True)
    return num_messages, num_senders, mean_processing_time, max_deviation, failure_rate


def _parse_int_arg(arg: str, arg_name: str, req_positive: bool = False) -> int:
    try:
        value = int(arg)
    except ValueError:
        print(f'Error: {arg_name} must be an integer')
        sys.exit(1)
    if req_positive and value < 1:
        print(f'Error: {arg_name} must be a positive integer')
        sys.exit(1)
    return value


def _parse_float_arg(arg: str, arg_name: str, req_non_negative: bool = False) -> float:
    try:
        value = float(arg)
    except ValueError:
        print(f'Error: {arg_name} must be a float')
        sys.exit(1)
    if req_non_negative and value < 0:
        print(f'Error: {arg_name} must be a non-negative float')
        sys.exit(1)
    return value


if __name__ == '__main__':
    USAGE = 'python3 start.py <num_messages> <num_senders> <mean_processing_time> <max_deviation> <failure_rate>'
    if len(sys.argv) != 6:
        print('Error: Invalid number of arguments')
        print(f'Usage: {USAGE}')
        sys.exit(1)

    run_simulation(*_process_args())
