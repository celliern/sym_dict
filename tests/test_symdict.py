#!/usr/bin/env python
# coding=utf8

import copy
import pickle

import pytest
from sym_dict import SymDict
from sympy import S, Symbol


@pytest.fixture()
def sdict():
    sdict = SymDict()
    sdict.add_relation('a - 2 * b')
    sdict.add_relation('c - b / 8')
    return sdict


@pytest.fixture()
def filled_sdict(sdict):
    sdict['a'] = 5
    return sdict


def test_rel(sdict):
    assert S('a - 2 * b') in [rel.rel for rel in sdict.magic_relations]
    assert S('c - b / 8') in [rel.rel for rel in sdict.magic_relations]


def test_atoms(sdict):
    assert ({Symbol(atom) for atom in ('a', 'b')}
            in [rel.atoms for rel in sdict.magic_relations])
    assert ({Symbol(atom) for atom in ('b', 'c')}
            in [rel.atoms for rel in sdict.magic_relations])


def test_missing(filled_sdict):
    assert filled_sdict['b'] == 5 / 2
    assert filled_sdict['c'] == 2.5 / 8
    assert filled_sdict['c'] == 5 / 2 / 8

    with pytest.raises(KeyError):
        filled_sdict['d']


def test_repr(filled_sdict):
    assert filled_sdict.__repr__() == dict(filled_sdict).__repr__()


def test_stored(filled_sdict):
    assert 'a' in filled_sdict.store


def test_deduced(filled_sdict):
    assert 'b' in filled_sdict.deduced
    assert 'c' in filled_sdict.deduced


def test_redefinition_key_stored(filled_sdict):
    filled_sdict['a'] = 10
    assert filled_sdict['b'] == 10 / 2
    assert filled_sdict['c'] == 5 / 8
    assert filled_sdict['c'] == 10 / 2 / 8


def test_redefinition_key_deduced(filled_sdict):
    filled_sdict['b'] = 10
    assert filled_sdict['b'] == 10
    assert filled_sdict['c'] == 10 / 8
    assert filled_sdict['a'] == 5


def test_redefinition_key_deduced_safe(filled_sdict):
    filled_sdict.safe = True
    with pytest.raises(KeyError):
        filled_sdict['b'] = 10


def test_redefinition_key_deduced_force(filled_sdict):
    del filled_sdict['a']
    filled_sdict['b'] = 10
    assert filled_sdict['b'] == 10
    assert filled_sdict['c'] == 10 / 8
    assert filled_sdict['a'] == 10 * 2


def test_len_filled_sym_dict(filled_sdict):
    assert len(filled_sdict) == 3


def test_len_empty_dict(sdict):
    assert len(sdict) == 0


def test_copy(filled_sdict):
    copied_filled_dict = filled_sdict.copy()
    assert copied_filled_dict == filled_sdict
    assert copied_filled_dict.safe == filled_sdict.safe
    assert copied_filled_dict.store == filled_sdict.store
    assert copied_filled_dict.deduced == filled_sdict.deduced
    assert copied_filled_dict.magic_relations == filled_sdict.magic_relations

    copied_filled_dict = copy.copy(filled_sdict)
    assert copied_filled_dict == filled_sdict
    assert copied_filled_dict.safe == filled_sdict.safe
    assert copied_filled_dict.store == filled_sdict.store
    assert copied_filled_dict.deduced == filled_sdict.deduced
    assert copied_filled_dict.magic_relations == filled_sdict.magic_relations

    copied_filled_dict = copy.deepcopy(filled_sdict)
    assert copied_filled_dict == filled_sdict
    assert copied_filled_dict.safe == filled_sdict.safe
    assert copied_filled_dict.store == filled_sdict.store
    assert copied_filled_dict.deduced == filled_sdict.deduced
    assert copied_filled_dict.magic_relations == filled_sdict.magic_relations


def test_pickle(filled_sdict):
    pickled_filled_dict = pickle.loads(pickle.dumps(filled_sdict))
    assert pickled_filled_dict == filled_sdict
    assert pickled_filled_dict.safe == filled_sdict.safe
    assert pickled_filled_dict.store == filled_sdict.store
    assert pickled_filled_dict.deduced == filled_sdict.deduced
    assert pickled_filled_dict.magic_relations == filled_sdict.magic_relations
