#!/usr/bin/python
"""Unique ID unit and integration tests."""
from __future__ import print_function
import unittest
import requests


class TestUniqueID(unittest.TestCase):
    """Test the uniqueid server end to end."""

    url = 'http://127.0.0.1:8051/getid?range={range}&mode={mode}'

    def _url(self, range, mode):
        """Return the parsed url."""
        return self.url.format(range=range, mode=mode)

    def test_working_stuff(self):
        """Test the good working bits."""
        req = requests.get(self._url(2, 'foo'))
        parts = req.json()
        self.assertTrue('endIndex' in parts)
        self.assertTrue('startIndex' in parts)
        self.assertEqual(parts['startIndex'], 1)
        self.assertEqual(parts['endIndex'], 2)

        req = requests.get(self._url(10, 'foo'))
        parts = req.json()
        self.assertTrue('endIndex' in parts)
        self.assertTrue('startIndex' in parts)
        self.assertEqual(parts['startIndex'], 3)
        self.assertEqual(parts['endIndex'], 12)

        req = requests.get(self._url('blah', 'foo'))
        self.assertEqual(req.status_code, 404)

        req = requests.get('http://127.0.0.1:8051/blah')
        self.assertEqual(req.status_code, 404)
