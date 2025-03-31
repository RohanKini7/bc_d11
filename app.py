from flask import Flask, render_template
from leaderboard import main

app = Flask(__name__)

@app.route("/")
def leaderboard():
    leaderboard_df = main(return_dataframe=True)
    leaderboard = leaderboard_df.to_dict(orient="records")
    return render_template("leaderboard.html", leaderboard=leaderboard)

if __name__ == "__main__":
    app.run(debug=True)