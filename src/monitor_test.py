import time
from queue import Queue
from typing import List
from unittest import TestCase

from src.monitor import Monitor, MonitorStatus
from src.producer import gen_msg_queue


class MonitorTest(TestCase):

    def test_monitor_no_msgs(self) -> None:
        output_q, failure_q = Queue(), Queue()  # type: (Queue, Queue)
        starting_ts = time.time()
        monitor = Monitor(output_q, failure_q, starting_ts, 1)
        status = monitor.status()
        self.assertEqual(status.num_msgs_sent, 0)
        self.assertEqual(status.num_msgs_failed, 0)
        self.assertEqual(status.avg_time_per_msg, 0)

    def test_monitor_with_msgs(self) -> None:
        output_q, failure_q = gen_msg_queue(20), gen_msg_queue(10)
        starting_ts = time.time()
        monitor = Monitor(output_q, failure_q, starting_ts, 1)
        statuses: List[MonitorStatus] = []
        statuses.append(monitor.status())
        time.sleep(0.01)
        statuses.append(monitor.status())
        time.sleep(0.01)
        monitor.stop()
        statuses.append(monitor.status())
        time.sleep(0.01)
        statuses.append(monitor.status())

        for status in statuses:
            self.assertEqual(status.num_msgs_sent, 20)
            self.assertEqual(status.num_msgs_failed, 10)

        self.assertGreater(statuses[1].avg_time_per_msg, statuses[0].avg_time_per_msg)
        self.assertGreater(statuses[2].avg_time_per_msg, statuses[1].avg_time_per_msg)

        # The last status should be the same as the previous one since the monitor was stopped
        self.assertEqual(statuses[3].avg_time_per_msg, statuses[2].avg_time_per_msg)

    def test_monitor_avg_time_per_msg_accuracy_one_sender(self) -> None:
        output_q, failure_q = gen_msg_queue(100), gen_msg_queue(100)
        starting_ts = time.time()
        monitor = Monitor(output_q, failure_q, starting_ts, 1)
        time.sleep(0.1)
        monitor.stop()
        status = monitor.status()
        self.assertAlmostEqual(status.avg_time_per_msg, 0.1 / 200, delta=0.01)

    def test_monitor_avg_time_per_msg_accuracy_multiple_senders(self) -> None:
        num_senders = 3
        output_q, failure_q = gen_msg_queue(100), gen_msg_queue(100)
        starting_ts = time.time()
        monitor = Monitor(output_q, failure_q, starting_ts, num_senders)
        time.sleep(0.1)
        monitor.stop()
        status = monitor.status()
        self.assertAlmostEqual(status.avg_time_per_msg, (0.1 / 200) / num_senders, delta=0.01)
