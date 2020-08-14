#!/bin/bash

if [ "$#" -ne "1" ]; then
    >&2 echo "usage: $(basename $0) <python_script>"
    exit 1
fi

SCRIPT=$1

#bandit -r $SCRIPT
black $SCRIPT
# E231: Missing whitespace after ',', ';', or ':'
# E501: Line too long (82 > 79 characters)
# W503: Line break occurred before a binary operator
# Line length == 88 is what black uses
flake8 --ignore=E231,E501,W503 --max-line-length=88 $SCRIPT

# Created by Mike Gilbert
