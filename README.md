# Pacifica Unique ID
[![Build Status](https://travis-ci.org/EMSL-MSC/pacifica-uniqueid.svg?branch=master)](https://travis-ci.org/EMSL-MSC/pacifica-uniqueid)

This is the pacifica unique ID generator API.

This service provides unique IDs for other pacifica services.

## The API

The Call:
```
curl http://localhost:8000/?range=10
```
The Response
```
{"endIndex": 18, "startIndex": 9}
```
