import pandas as pd
import json


# Load the CSV file into a DataFrame
with open('tourist_sites.json', 'r', encoding='utf-8') as f:
    tourist_sites = json.load(f)

print(tourist_sites['tour-eiffel']['name'])