# SMS Simulation Exercise

The objective is to simulate sending a large number of SMS alerts, like for an emergency alert service.

The simulation consists of three parts:
1. A producer that generates a configurable number of messages (default 1000) to random phone numbers. Each message
contains up to 100 random characters.

2. A configurable number of senders who pick up messages from the producer and simulate sending messages by waiting
a random period of time distributed around a configurable mean. Senders also have a configurable failure rate.

3. A progress monitor that displays the following and updates it every N seconds (configurable):
    - Number of messages sent so far
    - Number of messages failed so far
    - Average time per message so far
   
One instance each for the producer and the progress monitor will be started while a variable number of senders
can be started with different mean processing time and error rate settings.

You are free in the programming language you choose, but your code should come with reasonable unit testing.

Please submit the code test at least two business days before the interview, so we have time to review it.

## Architecture
In this implementation the Producer is a function that generates a Queue of messages with random phone numbers and text.

Senders run on separate threads and share the Input Queue generated by the Producer. They also share an Output Queue
where successful messages are placed and a Failure Queue where failed messages are placed. In addition, the Thread
Event used to stop the Senders is shared such that all Senders are stopped at the same time.

The Monitor shares the same Output Queue and Failure Queue as the Senders and monitors them to update the progress.

## Constraints
- Phone numbers are in the form xxx-xxx-xxxx, where 0-9 are valid digits in any position
- The text of messages is between 1 and 100 characters in length and consists of any printable ASCII characters

## Prerequisites
- `python3` is available on the environment PATH (Tested with Python 3.10)

## Scripts for installing dependencies and testing this project

NOTE: These scripts are intended for use on a *nix system or WSL on a Windows system.

WARNING: All scripts should be 'sourced' (i.e. `source ./script.sh` or `. ./script.sh`) to avoid failures and unexpected behaviors.

| Script           | Function                                                                                                                                                                                        |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| create_venv.sh   | Creates a virtual environment at `.venv` and installs the latest pip dependencies from `requirements.txt`                                                                                       |
| pin_reqs.sh      | Records the current dependency versions in `.venv` to `static_requirements.txt`                                                                                                                 |
| activate_venv.sh | Creates a virtual environment at `.venv` (if it doesn't exist) using `static_requirements.txt` and activates it                                                                                 |
| run_tests.sh     | Runs all unit tests in the project                                                                                                                                                              |
| lint.sh          | Lints the project ([Flake8](https://flake8.pycqa.org/en/4.0.1/) and [Mypy](https://mypy.readthedocs.io/en/stable/getting_started.html) must be installed and available on the environment PATH) |

## Running the simulation
Activate the virtual environment:
```shell
. ./activate_venv.sh  # or source ./activate_venv.sh
```

Run the simulation:
```shell
python3 start.py <num_messages> <num_senders> <mean_processing_time> <max_deviation> <failure_rate>

example:
python3 start.py 10000 4 0.01 0.001 0.2
```
Starts the simulation with 10000 messages, 4 senders, a mean message processing time of 0.01 seconds with a max
deviation in message processing time of 0.001 seconds, and a message failure rate of 0.2 (i.e. 20%).
