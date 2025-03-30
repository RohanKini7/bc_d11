import pandas as pd
import os
from glob import glob

data_folder = 'bc_d11/matches'

def get_match_files(folder):
    return sorted(glob(os.path.join(folder, '*.xlsx')))


def process_match(file):
    df = pd.read_excel(file)
    max_score = df['Points'].max()
    df['Normalized'] = (df['Points'] / max_score) * 100
    df = df.sort_values(by='Points', ascending=False).reset_index(drop=True)

    f1_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    df['F1_bonus'] = 0
    for i in range(min(len(df), len(f1_points))):
        df.at[i, 'F1_bonus'] = f1_points[i]

    df['Match_Score'] = (df['Normalized'] + df['F1_bonus']).round(2)
    return df


def create_player_record():
    return {
        'Total_Score': 0,
        'Wins': 0,
        'Podiums': 0,
        'Bottom3': 0,
        'Recent_Scores': []
    }


def update_leaderboard(df, leaderboard):
    for i, row in df.iterrows():
        player = row['Player']
        score = row['Match_Score']

        if player not in leaderboard:
            leaderboard[player] = create_player_record()

        leaderboard[player]['Total_Score'] += score
        leaderboard[player]['Recent_Scores'].append(score)
        if len(leaderboard[player]['Recent_Scores']) > 5:
            leaderboard[player]['Recent_Scores'].pop(0)

        if i == 0:
            leaderboard[player]['Wins'] += 1

        if i < 3:
            leaderboard[player]['Podiums'] += 1

        if i >= len(df) - 3:
            leaderboard[player]['Bottom3'] += 1

    return leaderboard


def leaderboard_to_dataframe(leaderboard):
    return pd.DataFrame([
        {
            'Player': player,
            'Total_Score': round(data['Total_Score'], 2),
            'Wins': data['Wins'],
            'Podiums': data['Podiums'],
            'Bottom3': data['Bottom3'],
            'Recent_Scores': data['Recent_Scores']
        } for player, data in leaderboard.items()
    ]).sort_values(by='Total_Score', ascending=False)


def main(return_dataframe=False):
    leaderboard = {}
    match_files = get_match_files(data_folder)

    for file in match_files:
        match_df = process_match(file)
        leaderboard = update_leaderboard(match_df, leaderboard)

    leaderboard_df = leaderboard_to_dataframe(leaderboard)

    if return_dataframe:
        return leaderboard_df
    else:
        print(leaderboard_df)