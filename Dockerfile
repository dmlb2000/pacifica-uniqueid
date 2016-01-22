FROM python:2-onbuild
EXPOSE 8051
CMD [ "python", "./FileIndexServer.py" ]
