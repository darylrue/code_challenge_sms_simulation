from random import randint, choice
from string import printable


def rand_digit() -> int:
    """Return a random digit between 0 and 9."""
    return randint(0, 9)

def rand_phone_number() -> str:
    """Return a random phone number in the format 'xxx-xxx-xxxx' where 0-9 are valid digits in any position."""
    r = rand_digit
    return f'{r()}{r()}{r()}-{r()}{r()}{r()}-{r()}{r()}{r()}{r()}'

def rand_text() -> str:
    """Return a random text string between 1 and 100 characters in length where each character is from the
    printable ASCII set."""
    num_chars = randint(1, 100)
    return ''.join([choice(printable) for _ in range(num_chars)])
