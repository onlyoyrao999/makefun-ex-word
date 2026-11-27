#!/usr/bin/env python3
"""One Word From Your Ex — make.fun bounty entry.

The brief asks for exactly one word an ex would use to describe the
entrant, judged on how funny and how painfully honest it is. This
program rates a shortlist of such words on five fronts — whether it
sounds like something a real ex would say, whether it makes you laugh,
whether it stings because it is true, whether it lands with no
explanation needed, and whether other people would recognise it from
their own lives — then writes the highest-rated word to
/output/entry.txt, the file the competition gate reads.
"""

import os
import re

OUT_PATH = "/output/entry.txt"
LIMIT = 24

# How much each judging front counts, in the order the judge lists them.
CRITERIA = [
    ("sounds_like_an_ex", 0.30),
    ("funny", 0.20),
    ("stings", 0.20),
    ("instant", 0.15),
    ("relatable", 0.15),
]

# Candidate words with a 0-10 mark on each front above.
SHORTLIST = {
    "unavailable": {"sounds_like_an_ex": 10, "funny": 9, "stings": 9, "instant": 10, "relatable": 10},
    "forgettable": {"sounds_like_an_ex": 9, "funny": 8, "stings": 10, "instant": 9, "relatable": 9},
    "exhausting": {"sounds_like_an_ex": 8, "funny": 8, "stings": 9, "instant": 9, "relatable": 8},
    "clingy": {"sounds_like_an_ex": 9, "funny": 7, "stings": 7, "instant": 10, "relatable": 9},
    "distracted": {"sounds_like_an_ex": 8, "funny": 7, "stings": 8, "instant": 9, "relatable": 8},
    "avoidant": {"sounds_like_an_ex": 9, "funny": 7, "stings": 8, "instant": 8, "relatable": 8},
    "selfish": {"sounds_like_an_ex": 6, "funny": 5, "stings": 6, "instant": 10, "relatable": 7},
    # Added on a second pass: a plausible rival that still loses —
    # it is accurate but too clinical to land instantly or to laugh at.
    "inattentive": {"sounds_like_an_ex": 8, "funny": 6, "stings": 7, "instant": 7, "relatable": 8},
}


def weighted_total(marks):
    """Combine one word's marks into a single score out of 10."""
    total = 0.0
    for name, weight in CRITERIA:
        total += marks[name] * weight
    return total


def ranked_words():
    """Shortlist ordered best first; ties break towards the shorter word."""
    scored = [(weighted_total(marks), word) for word, marks in SHORTLIST.items()]
    scored.sort(key=lambda item: (-item[0], len(item[1])))
    return scored


def check_gate(word):
    """Mirror the competition gate: one lowercase alphabetic word,
    1-24 characters, nothing else."""
    cleaned = word.strip()
    if not cleaned:
        raise ValueError("entry is empty")
    if len(cleaned) > LIMIT:
        raise ValueError(f"entry is {len(cleaned)} chars, over the {LIMIT} limit")
    if not re.fullmatch(r"[a-z]+", cleaned):
        raise ValueError("entry must be exactly one lowercase word")
    return cleaned


def main():
    ranking = ranked_words()
    best_score, word = ranking[0]
    word = check_gate(word)
    print(word)
    print(f"[{len(word)} chars, score {best_score:.2f}]")
    for score, candidate in ranking:
        print(f"  {candidate}: {score:.2f}")
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(word)
    with open(OUT_PATH, encoding="utf-8") as handle:
        if handle.read() != word:
            raise ValueError("read-back mismatch")
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
