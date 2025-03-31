import pytest
import pandas as pd
from leaderboard import (
    calculate_f1_bonus,
    calculate_normalized_scores
)


def make_df(points):
    return pd.DataFrame({
        'Player': [chr(65 + i) for i in range(len(points))],
        'Points': points
    })


def test_no_tie():
    df = make_df([100, 90, 80, 70])
    df = calculate_f1_bonus(df)
    expected = [25, 18, 15, 12]  # Exact F1 points
    assert all(round(df.loc[i, 'F1_bonus'], 2) == expected[i] for i in range(len(df)))


def test_two_way_tie():
    df = make_df([100, 100, 90])
    df = calculate_f1_bonus(df)
    avg_top = (25 + 18) / 2  # 21.5
    assert round(df.loc[0, 'F1_bonus'], 2) == round(avg_top, 2)
    assert round(df.loc[1, 'F1_bonus'], 2) == round(avg_top, 2)
    assert round(df.loc[2, 'F1_bonus'], 2) == 15


def test_three_way_tie():
    df = make_df([100, 100, 100, 90])
    df = calculate_f1_bonus(df)
    avg_top3 = (25 + 18 + 15) / 3  # 19.33
    for i in range(3):
        assert round(df.loc[i, 'F1_bonus'], 2) == round(avg_top3, 2)
    assert round(df.loc[3, 'F1_bonus'], 2) == 12


def test_tie_beyond_f1_points():
    # Players tied at positions 9–12
    df = make_df([100, 95, 94, 93, 92, 91, 90, 89, 80, 80, 80, 80])
    df = calculate_f1_bonus(df)

    # Players 8–11 are tied for ranks 9–12 (only 2+1+1+0 points available)
    # From f1_points = [25,18,15,12,10,8,6,4,2,1]
    # Their bonus = (2+1) / 4 = 0.75 each
    for i in range(8, 12):
        assert round(df.loc[i, 'F1_bonus'], 2) == 0.75


def test_all_same_score():
    df = make_df([100] * 5)
    df = calculate_f1_bonus(df)
    avg_all = sum([25, 18, 15, 12, 10]) / 5
    for i in range(5):
        assert round(df.loc[i, 'F1_bonus'], 2) == round(avg_all, 2)


def test_with_normalization():
    df = make_df([100, 90, 80])
    df = calculate_normalized_scores(df)
    assert 'Normalized' in df.columns
    assert df.loc[0, 'Normalized'] == 100.0
    assert df.loc[2, 'Normalized'] == 80.0
