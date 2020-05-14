#!/usr/bin/env python3
from argparse import Namespace, ArgumentParser
from collections import Counter, defaultdict
from functools import lru_cache
from typing import List
from re import split
import argparse
import math
import sys


@lru_cache(maxsize=None)
def calculate_entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum(count / lns * math.log(count / lns, 2) for count in p.values())


def entropy_lines(lines: List[str]) -> float:
    all_lines = [l.strip() for l in lines]
    results = []
    while all_lines:
        line = all_lines.pop()
        if line:
            for w in split(r"[^\w]|_", line.lower()):
                entropy = calculate_entropy(w)
                if len(w) > 20 and entropy > 0:
                    results.append((round(entropy, 3), line))
    return results


def parse_options(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        prog="entropy", description=("Measure the entropy of a string"),
    )
    parser.add_argument("text", nargs="+", help="Text you want to calculate entropy")
    parser.add_argument(
        "-n", "--number", default=10, help="Display n largest entropy values"
    )
    return parser.parse_args(args)


def run(args: Namespace) -> None:
    n = abs(int(args.number))
    results = entropy_lines(args.text)
    for score, line in sorted(results)[-n:]:
        print(f"--- Line ---\n{line[:50]}...")
        print(f"Entropy: {score}")
        print(f"Length: {len(line)}")


if __name__ == "__main__":
    if sys.stdin.isatty():
        run(parse_options(sys.argv[1:]))
    else:
        lines = [l.strip() for l in sys.stdin]
        run(parse_options(sys.argv[1:] + lines))
