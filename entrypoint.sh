#!/bin/bash

uwsgi \
  --http-socket 0.0.0.0:8051 \
  --master \
  --die-on-term \
  --wsgi-file /usr/src/app/UniqueIDServer.py "$@"
