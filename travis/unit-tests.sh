#!/bin/bash
coverage run --include='uniqueid*' --include='UniqueIDServer' -p UniqueIDServer.py &
SERVER_PID=$!
coverage run --include='uniqueid*' -m pytest -v
kill -9 $SERVER_PID
wait
coverage combine -a .coverage*
coverage report --show-missing
codeclimate-test-reporter
