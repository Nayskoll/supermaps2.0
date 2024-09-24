from flask import Flask, render_template, request, jsonify, abort
import pandas as pd
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()  

# Load the CSV file into a DataFrame
csv_file = 'paris_activities_high_touristic.csv'
df = pd.read_csv(csv_file)

def calculate_matching_score(row, touristique, culturel, chill):
    # Normalize user inputs (1-5 scale) to match activity scores (1-10 scale)
    touristique_normalized = int(touristique) * 2  # Convert to 1-10 scale
    culturel_normalized = int(culturel) * 2  # Convert to 1-10 scale
    chill_normalized = int(chill) * 2  # Convert to 1-10 scale

    # Calculate custom weights using a quadratic function to emphasize extreme values (1 or 5)
    touristic_weight = ((int(touristique) - 3) ** 2) / 4  # Results in higher weight for 1 and 5
    cultural_weight = ((int(culturel) - 3) ** 2) / 4
    chill_weight = ((int(chill) - 3) ** 2) / 4

    # Calculate differences, introduce stronger penalties for mismatched scores
    touristic_diff = abs(row['touristic_score'] - touristique_normalized)
    cultural_diff = abs(row['cultural_score'] - culturel_normalized)
    chill_diff = abs(row['chill_score'] - chill_normalized)

    # Use exponential penalties to heavily penalize mismatches
    touristic_score = (100 - (touristic_diff ** 2)) * touristic_weight
    cultural_score = (100 - (cultural_diff ** 2)) * cultural_weight
    chill_score = (100 - (chill_diff ** 2)) * chill_weight

    # Calculate total score and normalize it
    total_score = touristic_score + cultural_score + chill_score
    max_possible_score = (touristic_weight + cultural_weight + chill_weight) * 100
    normalized_score = (total_score / max_possible_score) * 100 if max_possible_score != 0 else 0

    # Return the rounded score
    return round(normalized_score)


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
    
    # Calculate the matching score for each activity
    df['affinity_score'] = df.apply(lambda row: calculate_matching_score(row, touristique, culturel, chill), axis=1)

    # Sort activities by affinity score in descending order (higher scores are more relevant)
    sorted_df = df.sort_values(by='affinity_score', ascending=False)

    # Convert to a list of dictionaries for JSON serialization
    activities = sorted_df.to_dict(orient='records')

    # Return the activities as a JSON response
    return jsonify({'activities': activities})




# Charger les données JSON
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
