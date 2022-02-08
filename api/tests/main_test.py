import pytest
import sys
import numpy as np
sys.path.append('/home/oli/projects/wordle_vue_flask/api/wordle_helper')
from wordle import main
from wordle import open_words_len_5
from wordle import find_matches
from wordle import combinations_apply_axis
from wordle import combinations_pad
from unittest import mock

class MyMock:
    def mock_greys():
        # ['A', 'B', 'C']
        greys = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K']
        return greys
    def mock_yellows():
        # [('A', 0), ('B', 3), ('C', 1)]
        yellows = [('R', 0), ('O', 1), ('S', 2), ('T', 3),]
        return yellows
    def mock_greens():
        greens = [('E', 4),]
        # [('A', 0), ('B', 3), ('C', 1)]
        return greens
    def mock_combos_pre_apply_axis():
        return np.array([['S', 'T', 'O', 'R', 'E'],
                         ['T', 'R', 'E', 'E', 'S'],
                         ['F', 'R', 'E', 'S', 'H']])
    def mock_combos_post_apply_axis():
        return np.array(['STORE', 'TREES', 'FRESH'])

    def mock_words_len_5():
        return np.array(['STORE', 'TREES', 'FRESH', 'WHICH', 'THEIR',' WOULD'])

    def mock_combos_padded():
        return np.array(['STORE', 'TREES', 'FRESH', 0, 0, 0])

    def mock_matches():
        return ['STORE', 'TREES', 'FRESH']

def test_open_words_len_5_datatype(tmpdir):
    tmpfile = tmpdir.join('words.txt')
    with mock.patch(
        'builtins.open', mock.mock_open(
            read_data='test'
        ),
    ):
        return_data = open_words_len_5(tmpfile)
        assert isinstance(return_data, list)

def test_open_words_len_5_length(tmpdir):
    tmpfile = tmpdir.join('words.txt')
    with mock.patch(
        'builtins.open', mock.mock_open(
            read_data='yellow\nsnail\nbird'
        ),
    ):
        return_data = open_words_len_5(tmpfile)
        assert len(return_data) == 1

def test_open_words_len_5_upper(tmpdir):
    tmpfile = tmpdir.join('words.txt')
    with mock.patch(
        'builtins.open', mock.mock_open(
            read_data='yellow\nsnail\nbird'
        ),
    ):
        return_data = open_words_len_5(tmpfile)
        assert return_data == ['SNAIL']

def test_combinations_aplly_axis_shape_type():
    combinations = combinations_apply_axis(MyMock.mock_combos_pre_apply_axis())
    assert type(combinations) == np.ndarray
    assert combinations.shape == (3,)

def test_combinations_aplly_axis_data():
    combinations = combinations_apply_axis(MyMock.mock_combos_pre_apply_axis())
    expected = np.array(['STORE', 'TREES', 'FRESH'], dtype='<U5')
    assert np.testing.assert_array_equal(combinations, expected) is None

def test_combinations_pad_shape_type():
    words_len_5 = MyMock.mock_words_len_5()
    combos = MyMock.mock_combos_post_apply_axis()
    combinations = combinations_pad(words_len_5,combos)
    expected = np.array(['STORE', 'TREES', 'FRESH', 0, 0, 0], dtype='<U5')
    assert type(combinations) == np.ndarray
    assert combinations.shape == (6,)

def test_combinations_pad_data():
    words_len_5 = MyMock.mock_words_len_5()
    combos = MyMock.mock_combos_post_apply_axis()
    combinations = combinations_pad(words_len_5,combos)
    expected = np.array(['STORE', 'TREES', 'FRESH', 0, 0, 0], dtype='<U5')
    assert np.testing.assert_array_equal(combinations, expected) is None

def test_find_matches_shape_type():
    words_len_5 = MyMock.mock_words_len_5()
    combos = MyMock.mock_combos_padded()
    matches = find_matches(words_len_5, combos)
    expected = np.array(['STORE', 'TREES', 'FRESH'], dtype='<U5')
    assert np.testing.assert_array_equal(matches, expected) is None

def test_find_matches_data():
    words_len_5 = MyMock.mock_words_len_5()
    combos = MyMock.mock_combos_padded()
    matches = find_matches(words_len_5, combos)
    expected = np.array(['STORE', 'TREES', 'FRESH'], dtype='<U5')
    assert type(matches) == np.ndarray
    assert matches.shape == (3,)

@mock.patch('wordle.combinations_pad', return_value=MyMock.mock_combos_padded())
@mock.patch('wordle.combinations_apply_axis', return_value=MyMock.mock_combos_post_apply_axis())
@mock.patch('wordle.open_words_len_5', return_value=MyMock.mock_words_len_5())
def test_main(
    mock_open_words_len_5,
    mock_combos_post_apply_axis,
    mock_combos_padded
):
    return_data = main(MyMock.mock_greys(), MyMock.mock_yellows(), MyMock.mock_greens())
    expected = MyMock.mock_matches()
    assert isinstance(return_data, list)
    assert return_data == expected
