from flask import Flask, render_template
import pandas as pd
import os
from glob import glob

app = Flask(__name__)

def calculate_leaderboard():
    data_folder = 'matches'
    match_files = glob(os.path.join(data_folder, '*.xlsx'))
    leaderboard = {}

    for file in match_files:
        df = pd.read_excel(file)
        max_score = df['Points'].max()
        df['Normalized'] = (df['Points'] / max_score) * 100

        # Optional F1 bonus
        df = df.sort_values(by='Points', ascending=False).reset_index(drop=True)
        f1_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
        df['F1_bonus'] = 0
        for i in range(min(len(df), len(f1_points))):
            df.at[i, 'F1_bonus'] = f1_points[i]

        df['Match_Score'] = ((df['Normalized'] + df['F1_bonus'])).round(2)

        for _, row in df.iterrows():
            player = row['Player']
            score = row['Match_Score']
            leaderboard[player] = leaderboard.get(player, 0) + score

    leaderboard_df = pd.DataFrame(list(leaderboard.items()), columns=['Player', 'Total_Score'])
    leaderboard_df = leaderboard_df.sort_values(by='Total_Score', ascending=False)
    leaderboard_df = pd.DataFrame(list(leaderboard.items()), columns=['Player', 'Total_Score'])
    leaderboard_df['Total_Score'] = leaderboard_df['Total_Score'].round(2)
    return leaderboard_df

@app.route('/')
def home():
    leaderboard = calculate_leaderboard()
    leaderboard = leaderboard.sort_values(by='Total_Score', ascending=False)
    data = leaderboard.to_dict(orient='records')
    return render_template('leaderboard.html', leaderboard=data)

if __name__ == '__main__':
    app.run(debug=True)