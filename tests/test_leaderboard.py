import pytest
import pandas as pd
from leaderboard import (
    process_wide_format, calculate_normalized_score, apply_f1_bonus,
    update_leaderboard, leaderboard_to_dataframe, main
)

@pytest.fixture
def sample_wide_data():
    return pd.DataFrame({
        "Player": ["A", "B", "C"],
        "Match1": [100, 80, 60],
        "Match2": [90, 70, 50]
    })

@pytest.fixture
def long_format_data():
    return pd.DataFrame({
        "Player": ["A", "B", "C"],
        "Points": [100, 80, 60]
    })

def test_process_wide_format(sample_wide_data: pd.DataFrame):
    df_long = process_wide_format(sample_wide_data)
    assert df_long.shape == (6, 3)
    assert set(df_long.columns) == {"Player", "Match", "Points"}

def test_calculate_normalized_score(long_format_data: pd.DataFrame):
    df_norm = calculate_normalized_score(long_format_data)
    assert "Normalized" in df_norm.columns
    assert df_norm.loc[0, "Normalized"] == 100.0
    assert df_norm.loc[2, "Normalized"] == 60.0

def test_apply_f1_bonus():
    df = pd.DataFrame({"Player": ["A", "B", "C"], "Points": [100, 100, 80]})
    df = apply_f1_bonus(df)
    assert "F1_bonus" in df.columns
    assert df[df['Points'] == 100].iloc[0]['F1_bonus'] == 21.5  # (25+18)/2
    assert df[df['Points'] == 80].iloc[0]['F1_bonus'] == 15

def test_update_leaderboard():
    df = pd.DataFrame({
        "Player": ["A", "B", "C"],
        "Normalized": [100, 80, 60],
        "F1_bonus": [25, 18, 15]
    })
    leaderboard = {}
    updated = update_leaderboard(df, leaderboard)
    assert updated["A"]["Total_Score"] == 125
    assert updated["B"]["Wins"] == 0
    assert updated["A"]["Wins"] == 1
    assert updated["C"]["Bottom3"] == 1

def test_leaderboard_to_dataframe():
    leaderboard = {
        "A": {"Total_Score": 125, "Wins": 1, "Podiums": 1, "Bottom3": 0, "Recent_Scores": [125]},
        "B": {"Total_Score": 98, "Wins": 0, "Podiums": 1, "Bottom3": 0, "Recent_Scores": [98]},
        "C": {"Total_Score": 75, "Wins": 0, "Podiums": 1, "Bottom3": 1, "Recent_Scores": [75]}
    }
    df = leaderboard_to_dataframe(leaderboard)
    assert list(df.columns) == ["Player", "Total_Score", "Wins", "Podiums", "Bottom3", "Recent_Scores"]
    assert df.iloc[0]["Player"] == "A"

def test():
    main(return_dataframe=False)
