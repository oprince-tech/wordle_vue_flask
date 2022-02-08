from __future__ import annotations

import numpy as np  # type: ignore


def open_words_len_5(file: str) -> list:
    with open(file, 'r') as f:
        rl = f.readlines()
        lines = [k.strip().upper() for k in rl if len(k) == 6]
        return lines


def combinations_apply_axis(combos):
    combinations = np.apply_along_axis(''.join, 1, combos)
    return combinations


def combinations_pad(words_len_5, combos):
    combinations = np.pad(
        combos, (
            0, abs(
                len(words_len_5) - combos.size,
            ),
        ), 'constant',
    )
    return combinations


def find_matches(words_len_5, combos):
    matches = np.intersect1d(words_len_5, combos)
    matches = matches[
        np.where(matches == words_len_5[:, None])[1]  # type: ignore
    ]
    return matches


def main(greys: list, yellows: list, greens) -> list:
    words_len_5_list = open_words_len_5('wiki-100k-strip-no-dups.txt')
    words_len_5_np = np.asarray(words_len_5_list)
    # words_len_5_np
    # array(['WHICH', 'THEIR',' WOULD']
    combinations = np.load('combinations.npy')
    if greys:
        for grey in greys:
            combinations = combinations[~np.any(combinations == grey, axis=1)]
    if yellows:
        for yellow in yellows:
            combinations = combinations[
                np.any(
                    (combinations == yellow[0]), axis=1,
                )
            ]
            combinations = np.delete(
                combinations, np.where(
                    combinations[:, yellow[1]] == yellow[0],
                ), axis=0,
            )
    if greens:
        for green in greens:
            combinations = combinations[
                np.where(
                    combinations[:, green[1]] == green[0],
                )
            ]
    # combinations
    # array([['A', 'B', 'C', 'D', 'E'],
    #        ['F', 'G', 'H', 'I', 'J']])
    combinations = combinations_apply_axis(combinations)
    combinations = combinations_pad(words_len_5_np, combinations)
    matches = find_matches(words_len_5_np, combinations)

    matches_list = matches.tolist()
    return matches_list
