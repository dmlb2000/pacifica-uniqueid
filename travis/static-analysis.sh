#!/bin/bash
pylint --rcfile=pylintrc UniqueIDServer.py DatabaseCreate.py uniqueid
radon cc *.py uniqueid
