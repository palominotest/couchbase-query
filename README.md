Couchbase Simple Query Tool
===========================

*Purpose: Connects to a couchbase instance and returns the contents of bucket given a key.*

Install Requirements
--------------------
`pip install -r requirements.txt`

Usage
-----
```
usage: query.py [-h] [-C CONFIG] [-H HOST] [-u USERNAME] [-p PASSWORD]
                [-b BUCKET] [-V VALUE]
                key

Couchbase Query Tool

positional arguments:
  key                   bucket key

optional arguments:
  -h, --help            show this help message and exit
  -C CONFIG, --config CONFIG
                        config file to load options from (default: None)
  -H HOST, --host HOST  host (default: localhost:8091)
  -u USERNAME, --username USERNAME
                        username (default: default)
  -p PASSWORD, --password PASSWORD
                        password (default: )
  -b BUCKET, --bucket BUCKET
                        bucket (default: default)
  -V VALUE, --value VALUE
                        value of key to set to (default: None)
```

Tests
-----
To run test writes and reads:
```
python tests.py
```