from flask import Flask, render_template
import leaderboard
app = Flask(__name__)

@app.route('/')
def home():
    leaderboard_data = leaderboard.main(return_dataframe=True)
    return render_template('leaderboard.html', leaderboard=leaderboard_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)