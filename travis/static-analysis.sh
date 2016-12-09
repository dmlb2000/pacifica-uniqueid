#!/bin/bash
pylint --rcfile=pylintrc UniqueIDServer.py uniqueid
radon cc *.py uniqueid
