from unittest import TestCase

from src.validations import is_valid_phone_number, is_valid_text


class ValidationsTest(TestCase):

    def test_valid_phone_number(self) -> None:
        self.assertTrue(is_valid_phone_number('123-456-7890'))

    def test_invalid_phone_number(self) -> None:
        self.assertFalse(is_valid_phone_number(None))  # type: ignore[arg-type]
        self.assertFalse(is_valid_phone_number(''))
        self.assertFalse(is_valid_phone_number('123-456-789'))
        self.assertFalse(is_valid_phone_number('123-456-78901'))
        self.assertFalse(is_valid_phone_number('123.456-7890'))
        self.assertFalse(is_valid_phone_number('123-456.7890'))
        self.assertFalse(is_valid_phone_number('a23-456-7890'))
        self.assertFalse(is_valid_phone_number('1a3-456-7890'))
        self.assertFalse(is_valid_phone_number('12a-456-7890'))
        self.assertFalse(is_valid_phone_number('123-a56-7890'))
        self.assertFalse(is_valid_phone_number('123-4a6-7890'))
        self.assertFalse(is_valid_phone_number('123-45a-7890'))
        self.assertFalse(is_valid_phone_number('123-456-a890'))
        self.assertFalse(is_valid_phone_number('123-456-7a90'))
        self.assertFalse(is_valid_phone_number('123-456-78a0'))
        self.assertFalse(is_valid_phone_number('123-456-789a'))

    def test_valid_text(self) -> None:
        self.assertTrue(is_valid_text('This is valid text.'))
        self.assertTrue(is_valid_text('a'))

    def test_invalid_text(self) -> None:
        self.assertFalse(is_valid_text(None))  # type: ignore[arg-type]
        self.assertFalse(is_valid_text(''))
        self.assertFalse(is_valid_text('abc\x01'))
        self.assertFalse(is_valid_text('This text has too many characters because its length is greater than 100.'
                                       ' Its length is actually 101.'))
