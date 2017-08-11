#!/bin/bash -xe
export MYSQL_ENV_MYSQL_USER=root
export MYSQL_ENV_MYSQL_PASSWORD=
coverage erase
rm -vf .coverage.*
export MYSQL_ENV_MYSQL_DATABASE=pacifica_uniqueid2
coverage run -p DatabaseCreate.py
export MYSQL_ENV_MYSQL_DATABASE=pacifica_uniqueid
sudo service mysql stop
# fail to connect
coverage run -p UniqueIDServer.py || true
sudo service mysql start
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
sudo service mysql stop
curl 'localhost:8051/getid?range=10&mode=file' || true
kill $SERVER_PID
wait

coverage combine -a .coverage.*
coverage report --show-missing --fail-under=100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
