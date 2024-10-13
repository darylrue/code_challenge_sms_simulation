#!/bin/sh

FILENAME="static_requirements.txt"

if [ ! -d .venv ]; then
  echo "Virtual environment not found. Have you run create_venv.sh?"
  exit 1
fi

. .venv/bin/activate
printf '\nPinning dependencies to %s/%s\n\n' "$PWD" "$FILENAME"
python3 -m pip freeze > $FILENAME
deactivate
printf '\nDependencies successfully written to %s\n\n' "$FILENAME"
