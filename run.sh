#!/usr/bin/env sh
set -e
set -a
source .env
set +a

.venv/bin/python3 run.py
