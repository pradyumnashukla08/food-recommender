import pandas as pd
from textblob import TextBlob
import difflib

# Load the dataset
food_data = pd.read_csv('data/food_data.csv')

# Mood analysis
def analyze_mood(mood_text):
    blob = TextBlob(mood_text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return 'Happy'
    elif sentiment < 0:
        return 'Sad'
    else:
        return 'Neutral'

# Recommender logic
def recommend_foods(location, weather, time, mood_text):
    mood = analyze_mood(mood_text)

    # Fuzzy match location
    available_locations = food_data['Location'].dropna().unique()
    closest = difflib.get_close_matches(location, available_locations, n=1, cutoff=0.6)

    if closest:
        matched_location = closest[0]
        location_matched_data = food_data[food_data['Location'].str.lower() == matched_location.lower()]
    else:
        location_matched_data = food_data.copy()  # fallback to full dataset (universal recommendation)

    # Filter based on weather, time, mood
    filtered = location_matched_data[
        ((location_matched_data['Weather'].str.lower() == weather.lower()) | (location_matched_data['Weather'].str.lower() == 'any')) &
        (location_matched_data['Time'].str.lower() == time.lower()) &
        ((location_matched_data['Mood'].str.lower() == mood.lower()) | (location_matched_data['Mood'].str.lower() == 'neutral'))
    ]

    # If no results, provide universal fallback recommendations
    if filtered.empty:
        fallback = food_data[
            (food_data['Location'].str.lower() == 'any') &
            (food_data['Time'].str.lower() == time.lower())
        ]
        return fallback if not fallback.empty else food_data.sample(5)  # last fallback: random 5 items

    return filtered
