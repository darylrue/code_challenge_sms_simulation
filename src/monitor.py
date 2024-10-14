import time
from queue import Queue
from typing import Optional

from src.message import Message


class MonitorStatus:
    def __init__(self,
                 num_msgs_sent: int,
                 num_msgs_failed: int,
                 avg_time_per_msg: float):
        """
        Represents the status of a Monitor, including the number of messages sent and failed, as well as the average
        time per message.

        :param num_msgs_sent: Number of messages sent
        :param num_msgs_failed: Number of messages failed
        :param avg_time_per_msg: Average time per message
        """
        self.num_msgs_sent: int = num_msgs_sent
        self.num_msgs_failed: int = num_msgs_failed
        self.avg_time_per_msg: float = avg_time_per_msg


class Monitor:
    def __init__(self,
                 output_q: Queue[Message],
                 failure_q: Queue[Message],
                 starting_timestamp: float,
                 num_senders: int):
        """
        Monitors the output queue and failure queue to determine the number of messages sent and failed, as well as
        the average time per message based on `starting_timestamp` and `num_senders`. When the `stop()` method is
        called, the elapsed time between the `starting_timestamp` and the current time is recorded and the calculated
        status output from the `status()` method becomes a fixed and final value.

        :param output_q: Queue to which successful messages are sent
        :param failure_q: Queue to which failed messages are sent
        :param starting_timestamp: Timestamp when message processing began (seconds since the epoch)
        :param num_senders: Number of senders sharing the `output_q` and the `failure_q`
        """
        if num_senders < 1:
            raise ValueError('num_senders must be a positive integer')
        self._output_q: Queue[Message] = output_q
        self._failure_q: Queue[Message] = failure_q
        self._starting_timestamp: float = starting_timestamp
        self._num_senders: int = num_senders
        self.final_status: Optional[MonitorStatus] = None

    def status(self) -> MonitorStatus:
        if self.final_status is not None:
            return self.final_status
        total_msgs = self._output_q.qsize() + self._failure_q.qsize()
        avg_sender_msgs = total_msgs / self._num_senders
        avg_msg_time = (time.time() - self._starting_timestamp) / avg_sender_msgs if avg_sender_msgs > 0 else 0
        return MonitorStatus(self._output_q.qsize(), self._failure_q.qsize(), avg_msg_time)

    def stop(self):
        self.final_status = self.status()
