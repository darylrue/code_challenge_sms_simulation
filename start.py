import sys

from src import simulation
from src.arg_parsing import parse_int_arg, parse_float_arg


def _process_args() -> tuple:
    num_messages = parse_int_arg(sys.argv[1], 'num_messages', req_positive=True)
    num_senders = parse_int_arg(sys.argv[2], 'num_senders', req_positive=True)
    mean_processing_time = parse_float_arg(sys.argv[3], 'mean_processing_time', req_non_negative=True)
    max_deviation = parse_float_arg(sys.argv[4], 'max_deviation', req_non_negative=True)
    failure_rate = parse_float_arg(sys.argv[5], 'failure_rate', req_non_negative=True)
    return num_messages, num_senders, mean_processing_time, max_deviation, failure_rate


if __name__ == '__main__':
    USAGE = 'python3 simulation.py <num_messages> <num_senders> <mean_processing_time> <max_deviation> <failure_rate>'
    if len(sys.argv) != 6:
        print('Error: Invalid number of arguments')
        print(f'Usage: {USAGE}')
        sys.exit(1)

    simulation.run(*_process_args())
