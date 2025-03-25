import pandas as pd
import os
from glob import glob

data_folder = 'matches'
match_files = glob(os.path.join(data_folder, '*.xlsx'))

# Initialize overall leaderboard
leaderboard = {}

for file in match_files:
    df = pd.read_excel(file)
    
    # Assuming your Excel has 'Player' and 'Points' columns
    max_score = df['Points'].max()

    # Normalize scores to a scale of 100
    df['Normalized'] = (df['Points'] / max_score) * 100

    # Add Formula 1 style points (Optional Bonus)
    df = df.sort_values(by='Points', ascending=False).reset_index(drop=True)
    f1_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

    df['F1_bonus'] = 0
    for i in range(min(len(df), len(f1_points))):
        df.at[i, 'F1_bonus'] = f1_points[i]

    # Calculate final score for the match
    df['Match_Score'] = (df['Normalized'] + df['F1_bonus']).round(2)

    # Aggregate to leaderboard
    for _, row in df.iterrows():
        player = row['Player']
        score = row['Match_Score']
        leaderboard[player] = leaderboard.get(player, 0) + score

# Convert leaderboard to DataFrame and sort
leaderboard_df = pd.DataFrame(list(leaderboard.items()), columns=['Player', 'Total_Score'])
leaderboard_df = leaderboard_df.sort_values(by='Total_Score', ascending=False)
leaderboard_df['Total_Score'] = leaderboard_df['Total_Score'].round(2)

print(leaderboard_df)