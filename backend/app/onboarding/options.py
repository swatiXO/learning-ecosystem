# Draft option lists for onboarding (PRD §6.1, PROJECT.md §6). Final lists are open
# decision D7 (keep/drop gender, area list granularity) — expect these to change without
# a migration, since nothing here is enforced by a DB CHECK constraint.

RELATIONSHIPS = ("mother", "father", "guardian", "teacher")

AREAS = (
    "karachi",
    "lahore",
    "islamabad",
    "rawalpindi",
    "faisalabad",
    "multan",
    "peshawar",
    "quetta",
    "other",
)

GRADES = (
    "playgroup",
    "nursery",
    "prep",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
)

# PRD §6.1 FR-2 #9.
LANGUAGES = ("urdu", "english", "punjabi", "pashto", "sindhi", "other")

GENDERS = ("male", "female", "other", "prefer_not_to_say")

# Placeholder avatar keys; the child can also pick on Day 1 (PRD FR-2 #11).
AVATARS = ("fox", "owl", "panda", "robot", "star")
