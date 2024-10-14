import queue
import time
from queue import Queue
from random import uniform
from threading import Event
from typing import Optional

from src.constants import MACHINE_MSG_PROC_TIME
from src.message import Message


class Sender:
    def __init__(self,
                 input_q: Queue[Message],
                 output_q: Queue[Message],
                 failure_q: Queue[Message],
                 stop_event: Optional[Event] = None,
                 mean_send_time: float = 0.25,
                 send_time_deviation: float = 0.1,
                 failure_rate: float = 0.05,
                 idle_wait_time: float = 0.25):
        """
        Simulates the sending of messages from the input queue to the output queue. Failed messages are sent to the
        failure queue, which is determined at random based on the failure rate. The time it takes to send a message is
        determined at random within the range of `mean_send_time +- send_time_deviation` with any non-positive number
        resulting in the message being sent immediately. The Sender processes messages one at a time and pulls a
        new message from the `input_q` immediately after processing the previous message. If `stop_event` is None,
        the Sender will stop when the `input_q` is empty. Otherwise, when message processing is complete and there is
        no new message available in the `input_q`, the Sender will wait `idle_wait_time` between checking `input_q`
        for new messages. When `stop_event` is set, the Sender finishes its current action and exists without fetching
        a new message from the `input_q`.

        :param input_q: Queue from which messages are fetched
        :param output_q: Queue to which successful messages are sent
        :param failure_q: Queue to which failed messages are sent
        :param stop_event: Event to stop the Sender from fetching new messages
        :param mean_send_time: Mean time to send a message
        :param send_time_deviation: Max possible deviation from the `mean_send_time`
        :param failure_rate: Rate of failure for sending messages between 0 (no failures) and 1 (all failures)
        :param idle_wait_time: Time between subsequent checks of the `input_q` for a new message while idle
        """
        self._input_q: Queue[Message] = input_q
        self._output_q: Queue[Message] = output_q
        self._failure_q: Queue[Message] = failure_q
        self._stop_event: Optional[Event] = stop_event
        self._send_time_max: float = mean_send_time + send_time_deviation
        self._send_time_min: float = mean_send_time - send_time_deviation
        self._failure_rate: float = failure_rate
        self._idle_wait_time: float = idle_wait_time
        self._start()

    def _start(self):
        if self._stop_event is None:
            # Process messages until the input queue is empty
            while not self._input_q.empty():
                try:
                    msg = self._input_q.get_nowait()
                    self._process_msg(msg)
                except queue.Empty:
                    pass
        else:
            # Process messages until the stop event is set
            while not self._stop_event.is_set():
                try:
                    msg = self._input_q.get_nowait()
                    self._process_msg(msg)
                except queue.Empty:
                    self._stop_event.wait(self._idle_wait_time)

    def _process_msg(self, msg: Message):
        wait_time = uniform(self._send_time_min, self._send_time_max) - MACHINE_MSG_PROC_TIME  # see src/constants.py
        if wait_time > 0:
            if self._stop_event is None:
                time.sleep(wait_time)
            else:
                self._stop_event.wait(wait_time)
        if uniform(0, 1) < self._failure_rate:
            self._failure_q.put(msg)
        else:
            self._output_q.put(msg)
