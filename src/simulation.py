import time
from queue import Queue
from threading import Thread, Event
from typing import List, Optional

from src import status_table
from src.message import Message
from src.producer import gen_msg_queue
from src.sender import Sender
from src.monitor import Monitor


def run(
        num_msgs: int,
        num_senders: int,
        mean_proc_time: float,
        max_deviation: float,
        failure_rate: float,
        display_update_secs: Optional[float] = None) -> None:
    """

    :param num_msgs: the number of messages to generate
    :param num_senders: the number of sender threads to start
    :param mean_proc_time: the mean processing time for a message
    :param max_deviation: the maximum deviation from the mean processing time
    :param failure_rate: the rate at which messages will fail (0.0 - 1.0)
    :param display_update_secs: the number of seconds to wait between updates to the display (Default: 0.75)
    :return: None
    """

    print(f'\nGenerating {num_msgs} messages...')
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

    # Pretty console output
    status_table.display(input_q, monitor, num_msgs, display_update_secs)

    print('All messages processed. Stopping senders...\n')
    stop_event.set()
    for thread in sender_threads:
        thread.join()
