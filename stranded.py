#!/usr/bin/env python3
"""Exact share of twenty-card deals with no way to 6 張 5 胡 but 將士象: python3 stranded.py

Such a hand holds no 暗刻 (no card three times), 兵卒 of at most one color,
and at most two 將帥.  These are the hands that must keep 缺將帥的士象.
The deck is 4 colors × 7 pieces × 4 copies; each color has one 將帥 and one 兵卒.
"""
from math import comb

# Ways to deal n cards with g 將帥 and b 兵卒 colors: state (n, g, b)
ways = {(0, 0, 0): 1}
for color in range(4):
    for piece in range(7):
        new = {}
        for (n, g, b), w in ways.items():
            for k in range(3):  # 0--2 copies, never a 暗刻
                state = (n + k, g + k * (piece == 0), b + (piece == 6 and k > 0))
                if state[0] <= 20 and state[1] <= 2 and state[2] <= 1:
                    new[state] = new.get(state, 0) + w * comb(4, k)
        ways = new

stranded = sum(w for (n, _, _), w in ways.items() if n == 20)
print(f"{stranded / comb(112, 20):.2%}")
