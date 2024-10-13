from src.errors import InvalidPhoneNumber, InvalidText
from src.validations import is_valid_phone_number, is_valid_text


class Message:
    # We may or may not need to validate the phone number and text depending on the source of the data.
    # If the source is external, we should validate the phone number and text. If the source is internal (and tested),
    # we can assume the phone number and text are valid and skip additional validation for efficiency.
    def __init__(self, phone_number: str, text: str):
        if not is_valid_phone_number(phone_number):
            raise InvalidPhoneNumber(f'{phone_number}')
        if not is_valid_text(text):
            raise InvalidText(f'{text}')
        self.phone_number = phone_number
        self.text = text
