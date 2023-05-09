from ..src.parts_parser import parse, split


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


def test_midline():
    # Test studies without laterality
    assert parse("CHEST") == 1
    assert parse("ABDOMEN") == 1
    assert parse("PELVIS") == 1
    assert parse("OPG") == 1
    assert parse("C SPINE") == 1
    assert parse("WHOLE SPINE") == 3
    assert parse("T L SPINE") == 2
    assert parse("T L SPINE SI JOINTS") == 3


def test_peripheral():
    # Test studies with laterality
    assert parse("R ELBOW") == 1
    assert parse("R THUMB") == 1
    assert parse("R FOOT") == 1
    assert parse("R FINGER") == 1
    assert parse("LEFT HAND") == 1
    assert parse("L TIB FIB") == 1
    assert parse("L TIB & FIB") == 1
    assert parse("BILATERAL HIPS") == 2
    assert parse("BILATERAL SHOULDERS") == 2
    assert parse("R FOOT HEEL") == 2
    assert parse("RIGHT ELBOW AND RADIUS") == 2
    assert parse("BILATERAL FEET ANKLES") == 4
    assert parse("BILATERAL FEMUR TIB FIB") == 4
    assert parse("BILATERAL HANDS FEET") == 4
    assert parse("BILATERAL FEET ANKLES") == 4


def test_composite():
    # Test composite studies
    assert parse("PELVIS LEG LENGTHS") == 2
    assert parse("RIGHT FOOT AND ANKLE") == 2
    assert parse("CHEST R HUMERUS") == 2
    assert parse("T SPINE BILATERAL FEET") == 3
    assert parse("CHEST PELVIS L SPINE") == 3
    assert parse("L SPINE PELVIS L KNEE") == 3
    assert parse("L SPINE SACRUM R FOOT") == 3
    assert parse("T L SPINE ABDOMEN") == 3
    assert parse("CHEST FACIAL BONES OPG MANDIBLE") == 4
    assert parse("CHEST R SC JOINT L SPINE SI JOINTS") == 4
    assert parse("CHEST C T L SPINE SI JOINTS") == 5
    assert parse("C SPINE BILATERAL WRISTS HANDS") == 5
    assert parse("CHEST BILATERAL HANDS FEET") == 5


def test_atypical_term():
    # Atypical terms
    assert parse("CERVICAL SPINE") == 1
    assert parse("R KNEE POST OP") == 1
    assert parse("LONG LEGS VIEWS L FEMUR") == 1
    assert parse("PELVIS ANKLE FOOT R14") == 3
    assert parse("CHEST L SHOULDER BILAT HANDS WRISTS FEET") == 8
