from unittest import TestCase

from src.producer import gen_msg_queue


class ProducerTest(TestCase):

    def test_q_gen_default(self) -> None:
        q = gen_msg_queue()
        self.assertTrue(q.full())
        self.assertTrue(q.qsize() == 1000)

    def test_q_gen_custom(self) -> None:
        q = gen_msg_queue(10)
        self.assertTrue(q.full())
        self.assertTrue(q.qsize() == 10)
