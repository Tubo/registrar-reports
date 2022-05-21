#!/usr/bin/env python3

from parser import parse, split

# test the division of parts
def len_split(s):
    return len(split(s))


def test_split_midline():
    assert len_split("CHEST") == 1
    assert len_split("ABDOMEN") == 1


def test_split_spine():
    assert len_split("WHOLE SPINE") == 1
    assert len_split("C SPINE") == 1
    assert len_split("T SPINE") == 1
    assert len_split("L SPINE") == 1
    assert len_split("S SPINE") == 1
    assert len_split("C T L SPINE") == 1


def test_split_peripheral():
    assert len_split("WRISTS HANDS FEET") == 1
    assert len_split("L FINGER") == 1
    assert len_split("LEFT TIB & FIB") == 1
    assert len_split("TIBIA FIBULA") == 1
    assert len_split("FINGER") == 1
    assert len_split("LUMBAR SPINE IN O.T. WITH O-ARM") == 1
    assert len_split("RIGHT KNEE POST OP") == 1
    assert len_split("R HIP FEMUR") == 1
    assert len_split("R WRIST ELBOW") == 1


def test_split_multiple():
    assert len_split("C SPINE ABDOMEN") == 2
    assert len_split("ABDOMEN C SPINE") == 2
    assert len_split("ABDOMEN C T SPINE") == 2
    assert len_split("ABDOMEN L S SPINE") == 2
    assert len_split("ABDOMEN C T L SPINE") == 2
    assert len_split("ABDOMEN WHOLE SPINE") == 2
    assert len_split("CHEST L HAND") == 2
    assert len_split("CHEST L HAND L SPINE") == 3
    assert len_split("CHEST L HAND L SPINE ABDOMEN") == 4
    assert len_split("CHEST BILATERAL HANDS L SPINE ABDOMEN") == 4
    assert len_split("CHEST BILATERAL HANDS L SPINE ABDOMEN") == 4
    assert len_split("CHEST BILATERAL HANDS WHOLE SPINE ABDOMEN") == 4
    assert len_split("R SHOULDER BILATERAL HANDS FEET") == 2
    assert len_split("LUMBAR SPINE IN O.T. WITH O-ARM R KNEE") == 2
    assert len_split("L SPINE SI JOINTS HIPS") == 3
