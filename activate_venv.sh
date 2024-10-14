#!/bin/sh

if [ ! -f static_requirements.txt ]; then
    printf '\nERROR: static_requirements.txt not found in %s. Have you run create_venv.sh and pin_reqs.sh?\n\n' "$PWD"
    exit 1
fi
if [ ! -d .venv ]; then
    printf '\nCreating Python virtual environment at %s/.venv\n' "$PWD"
    python3 -m venv .venv
    printf '\nActivating virtual environment\n'
    . .venv/bin/activate
    printf '\nUpgrading pip\n\n'
    python3 -m pip install --upgrade pip
    printf '\nInstalling dependencies from %s/static_requirements.txt\n\n' "$PWD"
    python3 -m pip install -r static_requirements.txt
    printf '\nPython virtual environment created and pip dependencies installed successfully\n\n'
else
    printf '\nPython virtual environment already exists at %s/.venv\n' "$PWD"
    printf '\nActivating virtual environment\n\n'
    . .venv/bin/activate
fi
