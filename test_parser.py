from parser import parse

# single vs. combo proportions
# trend with graph
# parser

# Test studies without laterality
assert parse("CHEST") == 1
assert parse("ABDOMEN") == 1
assert parse("PELVIS") == 1
assert parse("OPG") == 1
assert parse("C SPINE") == 1
assert parse("WHOLE SPINE") == 3
assert parse("T L SPINE") == 2
assert parse("T L SPINE SI JOINTS") == 3
# Test studies with laterality
assert parse("R ELBOW") == 1
assert parse("R THUMB") == 1
assert parse("R FOOT") == 1
assert parse("R FINGER") == 1
assert parse("LEFT HAND") == 1
assert parse("L TIB FIB") == 1
assert parse("BILATERAL HIPS") == 2
assert parse("BILATERAL SHOULDERS") == 2
assert parse("R FOOT HEEL") == 2
assert parse("RIGHT ELBOW AND RADIUS") == 2
assert parse("BILATERAL FEET ANKLES") == 4
assert parse("BILATERAL FEMUR TIB FIB") == 4
assert parse("BILATERAL HANDS FEET") == 4
assert parse("BILATERAL FEET ANKLES") == 4
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
# Atypical terms
assert parse("CERVICAL SPINE") == 1
assert parse("R KNEE POST OP") == 1
assert parse("LONG LEGS VIEWS L FEMUR") == 1
assert parse("PELVIS ANKLE FOOT R14") == 3
assert parse("CHEST L SHOULDER BILAT HANDS WRISTS FEET") == 8
