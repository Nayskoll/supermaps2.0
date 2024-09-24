import requests
import os
from dotenv import load_dotenv
import pandas as pd
import time

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def get_unsplash_image(query):
    # Récupérer la clé API depuis les variables d'environnement
    api_key = os.getenv('UNSPLASH_ACCESS_KEY')
    
    # URL de base de l'API Unsplash
    base_url = "https://api.unsplash.com/search/photos"
    
    # Paramètres de la requête
    params = {
        "query": query,
        "per_page": 1,  # Nous ne récupérons qu'une seule image
        "client_id": api_key
    }
    
    try:
        # Faire la requête à l'API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        
        # Analyser la réponse JSON
        data = response.json()
        
        # Vérifier si des résultats ont été trouvés
        if data['results']:
            # Récupérer l'URL de l'image
            image_url = data['results'][0]['urls']['regular']
            return image_url
        else:
            return "Aucune image trouvée pour cette requête."
    
    except requests.exceptions.RequestException as e:
        return f"Une erreur s'est produite lors de la requête : {e}"

# Exemple d'utilisation
#query = "Tour Eiffel"
#image_url = get_unsplash_image(query)
#print(f"URL de l'image pour '{query}': {image_url}")


# Load the CSV file into a DataFrame
csv_file = 'paris_activities_high_touristic.csv'
df = pd.read_csv(csv_file)


for index, row in df.iterrows():
    if index < 10:
        pass  # Arrête la boucle lorsque l'index atteint 40
    if index > 40:
        break  # Arrête la boucle lorsque l'index atteint 40
    query = row['name']  # Utilise le nom de l'activité comme requête
    new_url = get_unsplash_image(query)  # Obtient une nouvelle URL d'image
    df.at[index, 'image_url'] = new_url  # Met à jour l'URL dans le DataFrame
    print(new_url)
    time.sleep(1)

df.to_csv('paris_activities_high_touristic.csv', index=False, encoding='utf-8-sig')