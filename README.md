# Pacifica Unique ID
[![Build Status](https://travis-ci.org/EMSL-MSC/pacifica-uniqueid.svg?branch=master)](https://travis-ci.org/EMSL-MSC/pacifica-uniqueid)

This is the pacifica unique ID generator API.

This service provides unique IDs for other pacifica services.

## The API

The Call:
```
curl 'http://localhost:8000/?range=10&id=1'
```
The Response
```
{"endIndex": 9, "startIndex": 0}
```

Select different id to get different unique IDs

```
curl 'http://localhost:8000/?range=10&id=2'
curl 'http://localhost:8000/?range=10&id=3'
```
The Response
```
{"endIndex": 9, "startIndex": 0}
{"endIndex": 9, "startIndex": 0}
```

