#!/usr/bin/env python
# coding=utf8

import pytest
from sym_dict import SymDict

def test_add_rel():
    sdict = SymDict()
    sdict.add_relation('a - 2 * b')

