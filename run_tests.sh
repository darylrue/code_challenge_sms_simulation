#!/bin/sh

printf '\nRunning tests in %s/src...\n\n' "$PWD"
python3 -m unittest discover -s src -p '*_test.py' -v
printf '\n'
