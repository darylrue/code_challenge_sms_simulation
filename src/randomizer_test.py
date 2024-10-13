from string import printable
from unittest import TestCase
from src.randomizer import rand_digit, rand_phone_number, rand_text


NUM_ITERATIONS = 1000  # How many times to run each test case


class RandomizerTest(TestCase):

    def test_rand_digit(self):
        for _ in range(NUM_ITERATIONS):
            digit = rand_digit()
            self.assertTrue(0 <= digit <= 9)

    def test_rand_phone_number(self):
        for _ in range(NUM_ITERATIONS):
            phone_number = rand_phone_number()
            self.assertTrue(len(phone_number) == 12)
            self.assertTrue(phone_number[3] == '-')
            self.assertTrue(phone_number[7] == '-')

    def test_rand_text(self):
        for _ in range(NUM_ITERATIONS):
            text = rand_text()
            self.assertTrue(1 <= len(text) <= 100)
            for c in text:
                self.assertTrue(c in printable)
