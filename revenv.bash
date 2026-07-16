#!/bin/bash

rm -rf "$PWD/.venv/"
/usr/local/bin/python3 -m venv .venv
source .venv/bin/activate
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

