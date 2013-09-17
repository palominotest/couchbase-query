#!/usr/bin/env python
from copy import copy
import unittest
from unittest import TestCase
from couchbase.client import Couchbase
import query

HOST = 'localhost:8091'
USERNAME = 'default'
PASSWORD = ''


class QueryTest(TestCase):
    def setUp(self):
        cb = Couchbase(HOST, USERNAME, PASSWORD)
        self.cb = cb

        class Namespace(object):
            pass

        options = Namespace()
        options.host = HOST
        options.username = USERNAME
        options.password = PASSWORD
        options.bucket = 'default'
        self.options = options

    def tearDown(self):
        pass

    def test_write_and_read(self):
        # test writes
        opts = copy(self.options)
        opts.key = 'sandbox_one'
        opts.value = 'one'
        query.OPTIONS = opts
        query.main()
        self.assertTrue(query.LAST_DATA is None)
        opts = copy(self.options)
        opts.key = 'sandbox_two'
        opts.value = 'two'
        query.OPTIONS = opts
        query.main()
        self.assertTrue(query.LAST_DATA is None)

        # test reads
        opts = copy(self.options)
        opts.key = 'sandbox_one'
        opts.value = None
        query.OPTIONS = opts
        query.main()
        self.assertEquals(query.LAST_DATA, 'one')
        opts = copy(self.options)
        opts.key = 'sandbox_two'
        opts.value = None
        query.OPTIONS = opts
        query.main()
        self.assertEquals(query.LAST_DATA, 'two')


def main():
    unittest.main()


if __name__ == '__main__':
    main()