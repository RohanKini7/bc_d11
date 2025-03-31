import pytest
import pandas as pd
from leaderboard import (
    process_match,
    create_player_record,
    update_leaderboard,
    leaderboard_to_dataframe
)

# Sample test data to simulate a match
def sample_df():
    return pd.DataFrame({
        'Player': ['A', 'B', 'C'],
        'Points': [90, 80, 70]
    })


def test_process_match():
    df = sample_df()
    result_df = process_match(df)
    assert 'Normalized' in result_df.columns
    assert 'F1_bonus' in result_df.columns
    assert 'Match_Score' in result_df.columns
    assert result_df['Match_Score'].max() == 125


def test_create_player_record():
    record = create_player_record()
    assert record['Total_Score'] == 0
    assert record['Wins'] == 0
    assert record['Podiums'] == 0
    assert record['Bottom3'] == 0
    assert isinstance(record['Recent_Scores'], list)


def test_update_leaderboard():
    df = process_match(sample_df())
    leaderboard = {}
    leaderboard = update_leaderboard(df, leaderboard)
    assert 'A' in leaderboard
    assert leaderboard['A']['Total_Score'] > 0
    assert leaderboard['A']['Wins'] == 1
    assert leaderboard['C']['Bottom3'] == 1


def test_leaderboard_to_dataframe():
    df = process_match(sample_df())
    leaderboard = update_leaderboard(df, {})
    result_df = leaderboard_to_dataframe(leaderboard)
    assert isinstance(result_df, pd.DataFrame)
    assert 'Player' in result_df.columns
    assert 'Wins' in result_df.columns
    assert 'Podiums' in result_df.columns
    assert 'Bottom3' in result_df.columns
    assert 'Recent_Scores' in result_df.columns
