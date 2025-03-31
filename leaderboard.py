import pandas as pd
from supabase import create_client
import numpy as np
from supabase_config import URL, KEY, TABLE

def fetch_match_data():
    supabase = create_client(URL, KEY)
    response = supabase.table(TABLE).select("*").execute()
    data = response.data
    return pd.DataFrame(data)

def process_wide_format(df):
    df = df.replace({None: 0, np.nan: 0})  
    df = df.melt(id_vars=["Player"], var_name="Match", value_name="Points")
    return df

def create_player_record():
    return {
        'Total_Score': 0,
        'Wins': 0,
        'Podiums': 0,
        'Bottom3': 0,
        'Recent_Positions': []
    }

def calculate_normalized_score(df):
    max_score = df['Points'].max()
    df['Normalized'] = (df['Points'] / max_score) * 100 if max_score != 0 else 0
    return df

def apply_f1_bonus(df):
    f1_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    df = df.sort_values(by='Points', ascending=False).reset_index(drop=True)
    df['F1_bonus'] = 0

    i = 0
    rank = 0
    while i < len(df):
        tied_score = df.loc[i, 'Points']
        tied_players = df[df['Points'] == tied_score]
        n_tied = len(tied_players)
        bonus_slice = f1_points[rank:rank + n_tied]
        bonus_sum = sum(bonus_slice) if bonus_slice else 0
        avg_bonus = bonus_sum / n_tied if n_tied > 0 else 0

        for j in range(i, i + n_tied):
            if j < len(df):
                df.at[j, 'F1_bonus'] = avg_bonus

        i += n_tied
        rank += n_tied

    return df

def update_leaderboard(df, leaderboard):
    min_score = df[df['Points'] > 0]['Points'].min() if not df[df['Points'] > 0].empty else 0
    penalty_score = round((min_score * 0.7 / df['Points'].max()) * 100, 2) if df['Points'].max() != 0 else 0

    submitters_df = df[df['Points'] > 0].reset_index(drop=True)

    for i, row in df.iterrows():
        player = row['Player']
        submitted = row['Points'] > 0

        if not submitted:
            score = penalty_score
            position = "DNS"
        else:
            score = round(row['Normalized'] + row['F1_bonus'], 2)
            position = submitters_df[submitters_df['Player'] == player].index[0] + 1

        if player not in leaderboard:
            leaderboard[player] = create_player_record()

        leaderboard[player]['Total_Score'] += score
        leaderboard[player]['Recent_Positions'].append(position)
        if len(leaderboard[player]['Recent_Positions']) > 5:
            leaderboard[player]['Recent_Positions'].pop(0)

        if submitted:
            if position == 1:
                leaderboard[player]['Wins'] += 1
            if position <= 3:
                leaderboard[player]['Podiums'] += 1
            if position > len(submitters_df) - 3:
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
            'Recent_Positions': data['Recent_Positions']
        } for player, data in leaderboard.items()
    ]).sort_values(by='Total_Score', ascending=False)

def main(return_dataframe=False):
    raw_df = fetch_match_data()
    long_df = process_wide_format(raw_df)
    leaderboard = {}

    for match_name in long_df['Match'].unique():
        match_df = long_df[long_df['Match'] == match_name].copy()
        match_df = calculate_normalized_score(match_df)
        match_df = apply_f1_bonus(match_df)
        leaderboard = update_leaderboard(match_df, leaderboard)

    leaderboard_df = leaderboard_to_dataframe(leaderboard)

    if return_dataframe:
        return leaderboard_df
    else:
        print(leaderboard_df)

if __name__ == "__main__":
    main()
