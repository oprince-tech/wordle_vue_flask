import sys
from unittest import mock
sys.path.append('/home/oli/projects/wordle_vue_flask/api/wordle_helper')  # noqa

import numpy as np  # noqa: E402
import pytest  # noqa: E402
from wordle import combinations_apply_axis  # noqa: E402
from wordle import combinations_pad  # noqa: E402
from wordle import find_matches  # noqa: E402
from wordle import generate_combinations_save  # noqa: E402
from wordle import load_combinations  # noqa: E402
from wordle import main  # noqa: E402
from wordle import open_words_len_5  # noqa: E402


class MyMock:
    def mock_greys():  # type: ignore
        # ['A', 'B', 'C']
        return ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K']

    def mock_yellows():  # type: ignore
        # [('A', 0), ('B', 3), ('C', 1)]
        return [('R', 0), ('O', 1), ('S', 2), ('T', 3)]

    def mock_greens():  # type: ignore
        # [('A', 0), ('B', 3), ('C', 1)]
        return [('E', 4)]

    def mock_combos_pre_apply_axis():  # type: ignore
        return np.array([
            ['S', 'T', 'O', 'R', 'E'],
            ['T', 'R', 'E', 'E', 'S'],
            ['F', 'R', 'E', 'S', 'H'],
        ])

    def mock_combos_post_apply_axis():  # type: ignore
        return np.array(['STORE', 'TREES', 'FRESH'])

    def mock_words_len_5():  # type: ignore
        return np.array([
            'STORE', 'TREES', 'FRESH',
            'WHICH', 'THEIR', ' WOULD',
        ])

    def mock_combos_padded():  # type: ignore
        return np.array(['STORE', 'TREES', 'FRESH', 0, 0, 0])

    def mock_matches():  # type: ignore
        return ['STORE', 'TREES', 'FRESH']


@pytest.fixture
def mock_combos_pre_apply_axis():
    return np.array([
        ['S', 'T', 'O', 'R', 'E'],
        ['T', 'R', 'E', 'E', 'S'],
        ['F', 'R', 'E', 'S', 'H'],
    ])


@pytest.fixture
def mock_combos_post_apply_axis():
    return np.array(['STORE', 'TREES', 'FRESH'])


@pytest.fixture
def mock_words_len_5():
    return np.array([
        'STORE', 'TREES', 'FRESH',
        'WHICH', 'THEIR', ' WOULD',
    ])


@pytest.fixture
def mock_combos_padded():
    return np.array(['STORE', 'TREES', 'FRESH', 0, 0, 0])


def test_open_words_len_5_datatype(tmpdir):
    tmpfile = tmpdir.join('words.txt')
    with mock.patch(
        'builtins.open', mock.mock_open(
            read_data='test',
        ),
    ):
        return_data = open_words_len_5(tmpfile)
        assert isinstance(return_data, list)


def test_open_words_len_5_length(tmpdir):
    tmpfile = tmpdir.join('words.txt')
    with mock.patch(
        'builtins.open', mock.mock_open(
            read_data='yellow\nsnail\nbird',
        ),
    ):
        return_data = open_words_len_5(tmpfile)
        assert len(return_data) == 1


def test_open_words_len_5_upper(tmpdir):
    tmpfile = tmpdir.join('words.txt')
    with mock.patch(
        'builtins.open', mock.mock_open(
            read_data='yellow\nsnail\nbird',
        ),
    ):
        return_data = open_words_len_5(tmpfile)
        assert return_data == ['SNAIL']


def test_combinations_apply_axis_shape_type(mock_combos_pre_apply_axis):
    combinations = combinations_apply_axis(mock_combos_pre_apply_axis)
    assert type(combinations) == np.ndarray
    assert combinations.shape == (3,)


def test_combinations_apply_axis_data(mock_combos_pre_apply_axis):
    combinations = combinations_apply_axis(mock_combos_pre_apply_axis)
    expected = np.array(['STORE', 'TREES', 'FRESH'], dtype='<U5')
    assert np.testing.assert_array_equal(combinations, expected) is None


def test_combinations_pad_shape_type(
    mock_words_len_5,
    mock_combos_post_apply_axis,
):
    combinations = combinations_pad(
        mock_words_len_5, mock_combos_post_apply_axis,
    )
    assert type(combinations) == np.ndarray
    assert combinations.shape == (6,)


def test_combinations_pad_data(mock_words_len_5, mock_combos_post_apply_axis):
    combinations = combinations_pad(
        mock_words_len_5, mock_combos_post_apply_axis,
    )
    expected = np.array(['STORE', 'TREES', 'FRESH', 0, 0, 0], dtype='<U5')
    assert np.testing.assert_array_equal(combinations, expected) is None


def test_find_matches_shape_type(mock_words_len_5, mock_combos_padded):
    matches = find_matches(mock_words_len_5, mock_combos_padded)
    expected = np.array(['STORE', 'TREES', 'FRESH'], dtype='<U5')
    assert np.testing.assert_array_equal(matches, expected) is None


def test_find_matches_data(mock_words_len_5, mock_combos_padded):
    matches = find_matches(mock_words_len_5, mock_combos_padded)
    assert type(matches) == np.ndarray
    assert matches.shape == (3,)


@pytest.mark.parametrize(
    ('n_letters', 'shape'),
    [
        (1, (1, 1)),
        (2, (4, 2)),
        (3, (27, 3)),
        (4, (256, 4)),
        (5, (3125, 5)),
    ],
)
def test_generate_combinations_save_shape_type(n_letters, shape, tmpdir):
    file = tmpdir.join('combinations_test.npy')
    all_combinations = generate_combinations_save(file, letters=n_letters)
    assert type(all_combinations) == np.ndarray
    assert all_combinations.shape == shape


def test_generate_combinations_save_data(tmpdir):
    file = tmpdir.join('combinations_test.npy')
    all_combinations = generate_combinations_save(file, letters=3)
    assert all_combinations.shape == (27, 3)


def test_generate_combinations_save_saving(tmpdir):
    file = tmpdir.join('combinations_test.npy')
    generate_combinations_save(file, letters=3)
    file_content = np.load(str(file))
    assert file_content.shape == (27, 3)
    assert type(file_content) == np.ndarray


@mock.patch(
    'wordle.generate_combinations_save',
    return_value=MyMock.mock_combos_pre_apply_axis(),
)
def test_load_combinations_shape_type(mock_generate_combinations, tmpdir):
    file = tmpdir.join('combinations_test.npy')
    combinations = load_combinations(file)
    assert type(combinations) == np.ndarray
    assert combinations.shape == (3, 5)


@mock.patch(
    'wordle.combinations_pad',
    return_value=MyMock.mock_combos_padded(),
)
@mock.patch(
    'wordle.combinations_apply_axis',
    return_value=MyMock.mock_combos_post_apply_axis(),
)
@mock.patch(
    'wordle.open_words_len_5',
    return_value=MyMock.mock_words_len_5(),
)
def test_main(
    mock_open_words_len_5,
    mock_combos_post_apply_axis,
    mock_combos_padded,
):
    return_data = main(
        MyMock.mock_greys(),
        MyMock.mock_yellows(), MyMock.mock_greens(),
    )
    expected = MyMock.mock_matches()
    assert isinstance(return_data, list)
    assert return_data == expected
