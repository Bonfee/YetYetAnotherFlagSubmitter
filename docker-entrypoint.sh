#! /bin/sh

mongod &
sleep 2
python3 main.py
