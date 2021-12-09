import pytest
from lr import *


def test_1():
    start = "S"
    terms = ["a", "b"]
    non_terms = ["S"]
    Rules = ["S->aSbS", "S->"]
    LR = LR1_Parser()
    LR.fit(start, terms, non_terms, Rules)
    good = ["aababb"]
    bad = ["aabbba"]
    for i in good:
        if LR.predict(i) == 0:
            assert False
    for i in bad:
        if LR.predict(i) == 1:
            assert False
    assert True


def test_2():
    start = "S"
    terms = ["c", "d"]
    non_terms = ["S", "C"]
    Rules = ["S->CC", "C->cC", "C->d"]
    LR = LR1_Parser()
    LR.fit(start, terms, non_terms, Rules)
    good = ["cdd", "dd"]
    bad = ["cc", "dc"]
    for i in good:
        if LR.predict(i) == 0:
            assert False
    for i in bad:
        if LR.predict(i) == 1:
            assert False
    assert True


def test_3():
    start = "S"
    terms = ["a", "b"]
    non_terms = ["S"]
    Rules = ["S->aaS", "S->b"]
    LR = LR1_Parser()
    LR.fit(start, terms, non_terms, Rules)
    good = ["a" * 50 + "b", "a" * 16 + "b"]
    bad = ["a" * 20 + "ba", "a" * 9 + "b"]
    for i in good:
        if LR.predict(i) == 0:
            assert False
    for i in bad:
        if LR.predict(i) == 1:
            assert False
    assert True


def test_4():
    start = "S"
    terms = [str(i) for i in range(10)] + ["+", "-", "/", "*"]
    non_terms = ["S", "E"]
    Rules = ["S->E+E", "S->E-E", "S->E/E", "S->E*E"] + [f"E->{i}" for i in range(10)]
    print(Rules)
    LR = LR1_Parser()
    LR.fit(start, terms, non_terms, Rules)
    good = ["1*5", "1+6", "9-4", "8/9"]
    bad = ["1**5", "3/", "*5*"]
    for i in good:
        print(i)
        if LR.predict(i) == 0:
            assert False
    for i in bad:
        if LR.predict(i) == 1:
            assert False
    assert True


def test_5():
    start = "S"
    terms = ["a", "b", "c", "d"]
    non_terms = ["S", "D", "C"]
    Rules = ["S->Sa", "S->C", "S->SSb", "C->Dd", "D->cD", "D->"]
    LR = LR1_Parser()
    LR.fit(start, terms, non_terms, Rules)
    good = ["cdcdba", "ccccd", "d"]
    bad = ["cccdab", "c"]
    for i in good:
        if LR.predict(i) == 0:
            assert False
    for i in bad:
        if LR.predict(i) == 1:
            assert False
    assert True


def test_6():
    start = "S"
    terms = ["x", "y", "z", "=", ";"] + [str(i) for i in range(10)]
    non_terms = ["S", "I", "N"]
    Rules = ["S->I=N;"] + [f"N->{i}" for i in range(10)] + ["I->x", "I->y", "I->z"]
    LR = LR1_Parser()
    LR.fit(start, terms, non_terms, Rules)
    good = ["x=4;", "y=8;", "z=2;", "x=0;", "y=5;"]
    bad = ["x", "y", "z", "x=", "1=", "2="]
    for i in good:
        if LR.predict(i) == 0:
            assert False
    for i in bad:
        if LR.predict(i) == 1:
            assert False
    assert True
