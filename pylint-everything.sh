#!/bin/bash -xe

pylint *.py
coverage run --include='index_server*' index_server_unit_tests.py -v
coverage report -m
