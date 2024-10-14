#!/bin/sh

if [ -d .venv ]; then
    printf '\nRemoving existing virtual environment at %s/.venv\n' "$PWD"
    rm -rf .venv
fi

printf '\nCreating Python virtual environment at %s/.venv\n' "$PWD"
python3 -m venv .venv
. .venv/bin/activate
printf '\nUpgrading pip\n\n'
python3 -m pip install --upgrade pip
printf '\nInstalling dependencies from %s/requirements.txt\n\n' "$PWD"
python3 -m pip install -r requirements.txt
deactivate
printf '\nPython virtual environment created and pip dependencies installed successfully\n\n'
