from __future__ import annotations

import os

import numpy as np  # type: ignore


def open_words_len_5(file: str) -> list:
    with open(file, 'r') as f:
        rl = f.readlines()
        lines = [k.strip().upper() for k in rl if len(k) == 6]
        return lines


def generate_combinations_save(file: str, letters: int = 26) -> np.ndarray:
    alphabet = np.array([
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    ])
    all_combinations = np.empty((0, letters))
    for a in alphabet[:letters]:
        if letters >= 2:
            for b in alphabet[:letters]:
                if letters >= 3:
                    for c in alphabet[:letters]:
                        if letters >= 4:
                            for d in alphabet[:letters]:
                                if letters >= 5:
                                    for e in alphabet[:letters]:
                                        tmp = np.array([(a, b, c, d, e)])
                                        all_combinations = np.vstack(
                                            (all_combinations, tmp),
                                        )
                                else:
                                    tmp = np.array([(a, b, c, d)])
                                    all_combinations = np.vstack(
                                        (all_combinations, tmp),
                                    )
                        else:
                            tmp = np.array([(a, b, c)])
                            all_combinations = np.vstack(
                                (all_combinations, tmp),
                            )
                else:
                    tmp = np.array([(a, b)])
                    all_combinations = np.vstack((all_combinations, tmp))
        else:
            tmp = np.array([(a)])
            all_combinations = np.vstack((all_combinations, tmp))
    np.save(str(file), all_combinations)
    return all_combinations


def combinations_apply_axis(combos: np.ndarray) -> np.ndarray:
    combinations = np.apply_along_axis(''.join, 1, combos)
    return combinations


def combinations_pad(
    words_len_5: np.ndarray,
    combos: np.ndarray,
) -> np.ndarray:
    combinations = np.pad(
        combos, (
            0, abs(
                len(words_len_5) - combos.size,
            ),
        ), 'constant',
    )
    return combinations


def find_matches(words_len_5: np.ndarray, combos: np.ndarray) -> np.ndarray:
    matches = np.intersect1d(words_len_5, combos)
    matches = matches[
        np.where(matches == words_len_5[:, None])[1]  # type: ignore
    ]
    return matches


def load_combinations(file: str):
    if not os.path.isfile(file):
        combinations = generate_combinations_save(file, letters=5)
    else:
        combinations = np.load(file)
    return combinations


def main(greys: list, yellows: list, greens) -> list:
    combinations_file = 'combinations.npy'
    words_len_5_list = open_words_len_5('wiki-100k-strip-no-dups.txt')
    words_len_5_np = np.asarray(words_len_5_list)
    combinations = load_combinations(combinations_file)
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
