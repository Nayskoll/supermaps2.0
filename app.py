import pandas as pd
import json
from flask import Flask, render_template, request, jsonify, abort
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()  

# Load the CSV file into a DataFrame
csv_file = 'paris_activities_high_touristic.csv'
df = pd.read_csv(csv_file)

def calculate_matching_score(row, touristique, culturel, chill, popularity):
    # Scale user inputs from 1-5 range to 0-100 range
    touristique_normalized = int(touristique) * 20  # Scale to 0-100
    culturel_normalized = int(culturel) * 20        # Scale to 0-100
    chill_normalized = int(chill) * 20              # Scale to 0-100
    popularity_normalized = int(popularity) * 20    # Scale to 0-100

    # Calculate the absolute differences between user input and activity scores (0-100 scale)
    touristic_diff = abs(row['touristic_score'] - touristique_normalized)
    cultural_diff = abs(row['cultural_score'] - culturel_normalized)
    chill_diff = abs(row['chill_score'] - chill_normalized)
    popularity_diff = abs(row['popularity_score'] - popularity_normalized)

    # Apply a linear penalty by subtracting the difference from 100
    touristic_score = max(0, 100 - touristic_diff)
    cultural_score = max(0, 100 - cultural_diff)
    chill_score = max(0, 100 - chill_diff)
    popularity_score = max(0, 100 - popularity_diff) * 2

    # Average the scores to get the final matching score
    total_score = (touristic_score + cultural_score + chill_score + popularity_score) /  5

    # Return the rounded score, ensuring it's not negative
    return round(total_score)


@app.route('/')
def home():
    return render_template('results.html')


# Route to serve the Mapbox API key
@app.route('/api/key', methods=['GET'])
def get_api_key():
    api_key = os.getenv('MAPBOX_API_KEY')  # Store your Mapbox API key in an environment variable
    return jsonify({'apiKey': api_key})

@app.route('/update_activities', methods=['POST'])
def update_activities():
    # Get the user criteria from the AJAX request
    data = request.get_json()
    touristique = data.get('touristique')
    culturel = data.get('culturel')
    chill = data.get('chill')
    popularity = data.get('popularity')

    
    # Calculate the matching score for each activity
    df['affinity_score'] = df.apply(lambda row: calculate_matching_score(row, touristique, culturel, chill, popularity), axis=1)

    # Sort activities by affinity score in descending order (higher scores are more relevant)
    sorted_df = df.sort_values(by='affinity_score', ascending=False)

    # Convert to a list of dictionaries for JSON serialization
    activities = sorted_df.to_dict(orient='records')

    # Return the activities as a JSON response
    return jsonify({'activities': activities})


# Load the data from the JSON file
with open('tourist_sites.json', 'r', encoding='utf-8') as f:
    tourist_sites = json.load(f)

@app.route('/site/<site_slug>')
def site_detail(site_slug):
    site = tourist_sites.get(site_slug)
    if site:
        return render_template('site_detail.html', site=site)
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)