# Pacifica Unique ID 
[![Build Status](https://travis-ci.org/EMSL-MSC/pacifica-uniqueid.svg?branch=master)](https://travis-ci.org/EMSL-MSC/pacifica-uniqueid)

This is the pacifica unique ID generator API.

This service provides unique IDs for other pacifica services.

## The API

The Call:
```
curl 'http://localhost:8000/getid?range=10&mode=file'
```
The Response
```
{"endIndex": 9, "startIndex": 0}
```

Select a different mode to get different unique IDs.  Currently supported modes are 'file' and 'upload'

```
curl 'http://localhost:8000/getid?range=10&mode=file'
curl 'http://localhost:8000/getid?range=10&mode=upload'
```
The Response
```
{"endIndex": 9, "startIndex": 0}
{"endIndex": 9, "startIndex": 0}
```

