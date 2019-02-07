#!/usr/bin/env bash
git pull
make
pip3 install -r requirements.txt
python3 python/main.py