import re
from functools import lru_cache
from yaml import CLoader, load

from pyparsing import Group, Literal, OneOrMore, Or, FollowedBy, Keyword, Optional, Dict


with open("src/classifications.yaml") as f:
    classifications = load(f, Loader=CLoader)

with open("ce_descriptions.txt") as f:
    ce_descriptions = f.read()


def clean(s):
    spaced = re.sub(r"[^\w\s_]", " ", s).split()
    return " ".join(spaced)


def to_keywords(key):
    return [Keyword(w) for w in classifications[key]]


def ignore(_):
    return 0


def one(_):
    return 1


def two(_):
    return 2


def three(_):
    return 3


MIDLINES = Or(to_keywords("midline_parts")).setParseAction(one)

SPINE_PARTS = OneOrMore(Or(to_keywords("spine_parts"))).setParseAction(
    lambda t: len(t.asList())
)
SPINE_WHOLE = Literal("WHOLE")("whole").setParseAction(three)
SPINE = (SPINE_PARTS ^ SPINE_WHOLE) + FollowedBy("SPINE")

UNILATERAL = Or(to_keywords("unilateral")).setParseAction(ignore)
BILATERAL = Or(to_keywords("bilateral")).setParseAction(ignore)

DIGIT_NUM = Or(to_keywords("digit_number"))
DIGIT = Or(to_keywords("digit"))
DIGITS = Optional(DIGIT_NUM) + DIGIT

JOINT_NAME = Or(to_keywords("joints"))
JOINT = Literal("JOINT") ^ Literal("JOINTS")
JOINTS = JOINT_NAME + JOINT

PERIPHERAL_SINGULAR = (
    Or(to_keywords("singular_parts")) ^ DIGITS ^ JOINTS
).setParseAction(one)
PERIPHERAL_PLURAL = (
    Or(to_keywords("plural_parts")) ^ DIGITS ^ PERIPHERAL_SINGULAR ^ JOINTS
).setParseAction(two)

PERIPHERIES = (Optional(UNILATERAL) + PERIPHERAL_SINGULAR[1, ...]) ^ (
    Optional(BILATERAL) + PERIPHERAL_PLURAL[1, ...]
)

IGNORED = Or(to_keywords("ignore"))


pattern = MIDLINES ^ SPINE ^ PERIPHERIES
pattern.ignore(IGNORED)


def split(text):
    text = clean(text)
    result = pattern.searchString(text)
    return result.asList()


def calculate(list_of_parts):
    return sum(sum(i) for i in list_of_parts)


@lru_cache(maxsize=64)
def parse(text):
    return calculate(split(text))
