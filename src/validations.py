from string import printable


def is_valid_phone_number(phone_number: str) -> bool:
    """Return True if the phone number is in the format 'xxx-xxx-xxxx' where 0-9 are valid digits in any position,
    False otherwise."""
    if phone_number is None:
        return False
    if len(phone_number) != 12:
        return False
    if phone_number[3] != '-' or phone_number[7] != '-':
        return False
    for i in [0, 1, 2, 4, 5, 6, 8, 9, 10, 11]:
        if not phone_number[i].isdigit():
            return False
    return True


def is_valid_text(text: str) -> bool:
    """Return True if the text string is between 1 and 100 characters in length where each character is from the
    printable ASCII set, False otherwise."""
    if text is None:
        return False
    if not 1 <= len(text) <= 100:
        return False
    for c in text:
        if c not in printable:
            return False
    return True
