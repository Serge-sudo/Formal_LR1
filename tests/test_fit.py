import pytest
from lr import *


def test_1():
    flag = False
    start = "S"
    terms = ["a"]
    non_terms = ["S"]
    Rules = ["S->SS", "S->a"]
    LR = LR1_Parser()
    try:
        LR.fit(start, terms, non_terms, Rules)
    except Exception as e:
        if "Conflict" in str(e):
            flag = True
    if flag:
        assert True
    else:
        assert False


def test_2():
    flag = False
    start = "S"
    terms = ["a"]
    non_terms = ["S"]
    Rules = ["S->Sa", "S->a", "S->"]
    LR = LR1_Parser()
    try:
        LR.fit(start, terms, non_terms, Rules)
    except Exception as e:
        if "Conflict" in str(e):
            flag = True
    if flag:
        assert True
    else:
        assert False


def test_3():
    flag = False
    start = "S"
    terms = ["a", "b"]
    non_terms = ["S", "A", "B"]
    Rules = ["S->AB", "S->a", "S->", "B->BB", "B->b"]
    LR = LR1_Parser()
    try:
        LR.fit(start, terms, non_terms, Rules)
    except Exception as e:
        if "Conflict" in str(e):
            flag = True
    if flag:
        assert True
    else:
        assert False
