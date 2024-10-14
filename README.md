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


## Constraints
- Phone numbers are in the form xxx-xxx-xxxx, where 0-9 are valid digits in any position
- The text of messages is between 1 and 100 characters in length and consists of any printable ASCII characters

## Prerequisites
- `python3` is available on the environment PATH (Tested with Python 3.10)

## Scripts for installing dependencies and testing this project

NOTE: These scripts are intended for use on a *nix system or WSL on a Windows system.

| Script         | Function                                                                                                  |
|----------------|-----------------------------------------------------------------------------------------------------------|
| create_venv.sh | Creates a virtual environment at `.venv` and installs the latest pip dependencies from `requirements.txt` |
| pin_reqs.sh    | Records the current dependency versions in `.venv` to `static_requirements.txt`                           |
| run_tests.sh   | Runs all unit tests in the project                                                                        |

## Running the simulation
```shell
python3 src/start.py <num_messages> <num_senders> <mean_processing_time> <max_deviation> <failure_rate>

example:
python3 src/start.py 1000 4 0.01 0.001 0.2
```
Starts the simulation with 1000 messages, 4 senders, a mean message processing time of 0.01 seconds with a max
deviation in message processing time of 0.001 seconds, and a message failure rate of 0.2.