#!/usr/bin/env python3
"""One Word From Your Ex — make.fun bounty entry.

Scores a small table of candidate single words an ex would use to
describe the entrant on ex-voice (a word a real ex would actually say
about a former partner), funniness (surprise, a sharp turn, lands
harder than expected), sting (painfully true, and the entrant plainly
knows it), instantness (lands at once, needs no explanation, cannot be
swapped for a near synonym without losing its edge) and relatability
(names something people have lived through too), picks the best,
validates it against the competition gate (UTF-8 text of 1-24
characters, exactly one word, not only whitespace), prints it and
writes it to /output/entry.txt.
"""

import os

MAX_LEN = 24

# Each candidate: (word, ex_voice, funny, sting, instant, relatable)
# — scores out of 10.
CANDIDATES = [
    ("unavailable", 10, 9, 9, 10, 10),
    ("forgettable", 9, 8, 10, 9, 9),
    ("exhausting", 8, 8, 9, 9, 8),
    ("clingy", 9, 7, 7, 10, 9),
    ("distracted", 8, 7, 8, 9, 8),
    ("selfish", 6, 5, 6, 10, 7),
    ("avoidant", 9, 7, 8, 8, 8),
]

WEIGHTS = {
    "ex_voice": 0.30,
    "funny": 0.20,
    "sting": 0.20,
    "instant": 0.15,
    "relatable": 0.15,
}


def score(candidate):
    word, ex_voice, funny, sting, instant, relatable = candidate
    return (
        ex_voice * WEIGHTS["ex_voice"]
        + funny * WEIGHTS["funny"]
        + sting * WEIGHTS["sting"]
        + instant * WEIGHTS["instant"]
        + relatable * WEIGHTS["relatable"]
    )


def validate(word):
    """Gate check: 1-24 chars, exactly one word (no spaces, no
    punctuation, letters only), not only whitespace."""
    word = word.strip()
    if not word:
        raise ValueError("entry is empty")
    if len(word) > MAX_LEN:
        raise ValueError(f"entry is {len(word)} chars, over the 24 limit")
    if len(word.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if not word.isalpha():
        raise ValueError("entry must be a single alphabetic word")
    if word != word.lower():
        raise ValueError("entry must be lowercase")
    return word


def pick_best():
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    return ranked[0][0], score(ranked[0])


def main():
    word, best_score = pick_best()
    word = validate(word)
    print(word)
    print(f"[{len(word)} chars, score {best_score:.2f}]")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(word)
    with open("/output/entry.txt", encoding="utf-8") as f:
        assert f.read() == word, "read-back mismatch"
    print("wrote /output/entry.txt")


if __name__ == "__main__":
    main()
