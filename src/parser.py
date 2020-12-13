from pyparsing import Group, Literal, OneOrMore, Or, FollowedBy, Keyword
from yaml import CLoader, load

with open("src/classifications.yaml") as f:
    classifications = load(f, Loader=CLoader)

with open("ce_descriptions.txt") as f:
    ce_descriptions = f.read()


def to_keywords(key):
    return [Keyword(w) for w in classifications[key]]


MIDLINES = Or(to_keywords("midline"))

SPINE_PARTS = OneOrMore(Or(to_keywords("spine_parts")))
SPINE_WHOLE = Literal("WHOLE")
SPINE = Group(Group(SPINE_PARTS ^ SPINE_WHOLE) + Literal("SPINE"))

SINGLE = Or(to_keywords("single"))
DOUBLE = Or(to_keywords("double"))
DIGITS = Or(to_keywords("digit"))
PERIPHERAL_SINGULAR = Or(to_keywords("unilateral")) ^ DIGITS
PERIPHERAL_PLURAL = Or(to_keywords("bilateral")) ^ DIGITS
PERIPHERIES = Group(
    (SINGLE + PERIPHERAL_SINGULAR[1, ...])
    ^ (DOUBLE + PERIPHERAL_PLURAL[1, ...])
    ^ PERIPHERAL_SINGULAR[1, ...]
    ^ PERIPHERAL_PLURAL[1, ...]
)

pattern = OneOrMore(MIDLINES ^ SPINE ^ PERIPHERIES)


def split(text):
    result = pattern.parseString(text)
    print(result)
    return result.asList()


def parse(text):
    pass
