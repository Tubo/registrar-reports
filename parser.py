import re

CENTRAL_ORGANS = [
    r"FACIAL BONES",
    r"MANDIBLE",
    r"ORBITS?",
    r"(SOFT TISSUE |ST )?NECK",
    r"OPG",
    r"SKULL",
    # thorax
    r"CHEST|CXR",
    r"STERNUM",
    # abdomen
    r"ABDOMEN|ABDO",
    r"KUB",
    r"PELVIS",
    # spine
    r"(?:(C|CERVICAL)[ -])?(?:(T|THROACIC)[ -])?(?:(L|LUMBAR)[ -])?SPINE",
    r"WHOLE SPINE",
    r"SACRUM",
    r"COCCYX",
    r"SI JOINTS?",
]

SIDE_ORGANS = [
    r"TMJS?",
    r"COCHLEA IMPLANT",
    r"SINUS(ES)?",
    # upper limb
    r"SCAPHOIDS?",
    r"THUMBS?",
    r"(INDEX |MIDDLE |RING |LITTLE )*FINGERS?",
    r"WRISTS?",
    r"HANDS?",
    r"FOREARMS?",
    r"ELBOWS?",
    r"HUMER(US|I)",
    r"ARMS?",
    r"SHOULDERS?",
    r"SCAPULA",
    r"CLAVICLES?",
    r"AC",
    r"SC",
    r"UPPER LIMBS?",
    # lower limb
    r"HIPS?",
    r"FEMURS?",
    r"KNEES?",
    r"PATELLA",
    r"TIB ?FIB|TIBIA FIBULA",
    r"LEGS?",
    r"ANKLES?",
    r"FOOT|FEET",
    r"FOREFOOT",
    r"CALCANE(US|UM|I)",
    r"HEELS?",
    r"TOES?",
    r"LOWER LIMBS?",
]

MODIFIERS = [
    r"L|LEFT",
    r"R|RIGHT",
    r"BILAT|BILATERAL|BOTH",
]

PRESET = [r"SKELETAL SURVEY"]

central_organ_pattern = "|".join(CENTRAL_ORGANS)
modifiers = "|".join(MODIFIERS)
side_organ_pattern = "|".join(SIDE_ORGANS)
# preset = " ".join(PRESET)

PATTERN = f"({central_organ_pattern} |(({modifiers} )? ({side_organ_pattern} )+))+"


def parse(desc: str):
    r = re.findall(PATTERN, desc)
    print(r)
    return len(r)
