from flask import Flask, render_template, request
import pandas as pd
from model.recommender import recommend_foods

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user inputs
        location = request.form['location']
        weather = request.form['weather']
        time = request.form['time']
        mood = request.form['mood']

        # Get recommendations, now including location
        recommendations = recommend_foods(location, weather, time, mood)

        return render_template("index.html", recommendations=recommendations.to_dict(orient='records'))

    return render_template("index.html", recommendations=[])

if __name__ == "__main__":
    app.run(debug=True)
