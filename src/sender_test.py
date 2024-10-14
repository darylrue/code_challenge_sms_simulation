import time
import unittest
from queue import Queue
from threading import Event, Thread
from unittest import TestCase

from src.producer import gen_msg_queue
from src.sender import Sender


class SenderTest(TestCase):

    @unittest.skip("This test is time-based and machine-dependent and should not be run in CI/CD pipelines.")
    def test_processing_time(self):
        num_msgs = 10000
        input_q = gen_msg_queue(num_msgs)
        output_q, failure_q = Queue(), Queue()
        start_ts = time.time()
        mean_send_time = 0.0001
        Sender(input_q, output_q, failure_q, mean_send_time=mean_send_time, send_time_deviation=0.00001, failure_rate=0)
        elapsed_time = time.time() - start_ts
        self.assertAlmostEqual(mean_send_time, elapsed_time / num_msgs, delta=0.1)

    def test_failure_rate_zero(self):
        num_msgs = 10000
        input_q = gen_msg_queue(num_msgs)
        output_q, failure_q = Queue(), Queue()
        Sender(input_q, output_q, failure_q, mean_send_time=0, send_time_deviation=0, failure_rate=0)
        self.assertTrue(failure_q.empty())

    def test_failure_rate_max(self):
        num_msgs = 10000
        input_q = gen_msg_queue(num_msgs)
        output_q, failure_q = Queue(), Queue()
        Sender(input_q, output_q, failure_q, mean_send_time=0, send_time_deviation=0, failure_rate=1)
        self.assertTrue(failure_q.qsize() == num_msgs)

    def test_failure_rate_custom(self):
        num_msgs = 10000
        input_q = gen_msg_queue(num_msgs)
        output_q, failure_q = Queue(), Queue()
        failure_rate = 0.1
        Sender(input_q, output_q, failure_q, mean_send_time=0, send_time_deviation=0, failure_rate=failure_rate)
        actual_failure_rate = failure_q.qsize() / num_msgs
        self.assertAlmostEqual(failure_rate, actual_failure_rate, delta=0.1)

    def test_stop_event_before_finished(self):
        num_msgs = 10000
        input_q = gen_msg_queue(num_msgs)
        output_q, failure_q = Queue(), Queue()
        stop_event = Event()
        sender_thread = Thread(target=Sender, args=(input_q, output_q, failure_q, stop_event))
        sender_thread.start()
        stop_event.set()
        sender_thread.join()
        msgs_processed = output_q.qsize() + failure_q.qsize()
        self.assertTrue(msgs_processed < num_msgs)

    def test_stop_event_after_finished(self):
        num_msgs = 10
        input_q = gen_msg_queue(num_msgs)
        output_q, failure_q = Queue(), Queue()
        stop_event = Event()
        sender_thread = Thread(target=Sender, args=(input_q, output_q, failure_q, stop_event, 0, 0))
        sender_thread.start()
        time.sleep(0.01)
        stop_event.set()
        sender_thread.join()
        msgs_processed = output_q.qsize() + failure_q.qsize()
        self.assertTrue(msgs_processed == num_msgs)
