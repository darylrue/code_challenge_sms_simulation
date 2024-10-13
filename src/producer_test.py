from unittest import TestCase

from src.producer import Producer


class ProducerTest(TestCase):

    def test_instantiation_default(self):
        p = Producer()
        self.assertTrue(p.num_msgs == 1000)
        self.assertTrue(len(p.msgs) == 1000)
        self.assertTrue(p.current_msg_index == 0)

    def test_instantiation_custom(self):
        p = Producer(10)
        self.assertTrue(p.num_msgs == 10)
        self.assertTrue(len(p.msgs) == 10)
        self.assertTrue(p.current_msg_index == 0)

    def test_next(self):
        p = Producer(10)
        for i in range(10):
            self.assertTrue(p.has_next())
            msg = p.next()
            self.assertTrue(msg.phone_number is not None)
            self.assertTrue(msg.text is not None)
        self.assertTrue(p.current_msg_index == 10)
        self.assertTrue(p.next() is None)
        self.assertFalse(p.has_next())
