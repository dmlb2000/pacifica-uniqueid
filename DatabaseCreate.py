#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Create the unique index database schema."""
from uniqueid.orm import create_tables


if __name__ == '__main__':  # pragma: no cover
    create_tables()
