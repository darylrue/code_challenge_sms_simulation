#!/bin/sh

printf '\nRunning Flake8...\n'
flake8 --config tox.ini
printf '\nRunning Mypy...\n'
mypy --config-file tox.ini --explicit-package-bases src
