#!/bin/bash
coverage erase
rm -vf .coverage.*
docker-compose stop uniqueidmysql
# fail to connect
coverage run -p UniqueIDServer.py || true
docker-compose start uniqueidmysql
sleep 5
coverage run -p UniqueIDServer.py &
SERVER_PID=$!
while ! curl -s -o /dev/null localhost:8051
do
  sleep 1
done
coverage run -p -m pytest -v
kill $SERVER_PID
wait

# break mysql after successfully starting
coverage run -p UniqueIDServer.py &
SERVER_PID=$!
sleep 5
curl 'localhost:8051/getid?range=10&mode=file' || true
docker-compose stop uniqueidmysql
curl 'localhost:8051/getid?range=10&mode=file' || true
kill $SERVER_PID
wait

coverage combine -a .coverage.*
coverage report --show-missing
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
