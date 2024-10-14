from unittest import TestCase

from src.errors import InvalidPhoneNumber, InvalidText
from src.message import Message


class MessageTest(TestCase):

    def test_valid_instantiation(self) -> None:
        text = 'This is valid text.'
        phone_number = '123-456-7890'
        msg = Message(phone_number, text)
        self.assertTrue(msg.phone_number == phone_number)
        self.assertTrue(msg.text == text)

    def test_instantiation_with_invalid_phone_number(self) -> None:
        with self.assertRaises(InvalidPhoneNumber):
            Message('123-456-789', 'valid text')

    def test_instantiation_with_invalid_text(self) -> None:
        with self.assertRaises(InvalidText):
            Message('123-456-7890', '\x00')
