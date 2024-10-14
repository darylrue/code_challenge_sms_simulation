import sys


def parse_int_arg(arg: str, arg_name: str, req_positive: bool = False) -> int:
    try:
        value = int(arg)
    except ValueError:
        print(f'Error: {arg_name} must be an integer')
        sys.exit(1)
    if req_positive and value < 1:
        print(f'Error: {arg_name} must be a positive integer')
        sys.exit(1)
    return value


def parse_float_arg(arg: str, arg_name: str, req_non_negative: bool = False) -> float:
    try:
        value = float(arg)
    except ValueError:
        print(f'Error: {arg_name} must be a float')
        sys.exit(1)
    if req_non_negative and value < 0:
        print(f'Error: {arg_name} must be a non-negative float')
        sys.exit(1)
    return value
