from dotenv import load_dotenv
import os
from mistralai import Mistral


load_dotenv()  

api_key = os.getenv('MISTRAL_API_KEY') 

model = "mistral-large-latest"

client = Mistral(api_key=api_key)


with open('raw_text_bolivie.txt', 'r', encoding='utf-8', errors='replace') as file:
    texte_a_nettoyer = file.read()

# Définir le message système
system_message = "Vous êtes un assistant spécialisé dans le nettoyage et la structuration de textes touristiques. Votre tâche est de nettoyer le texte fourni en supprimant tout contenu non pertinent pour un guide de voyage, et de structurer les informations importantes. Garde toutes les informations"

# Définir le message utilisateur avec le texte à nettoyer
user_message = f"Nettoyez et structurez le texte suivant en ne gardant que les informations pertinentes pour un guide de voyage ou tout type de voyageur :\n\n{texte_a_nettoyer}"

# Créer la liste des messages pour le modèle de chat
messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message}
]

# Envoyer la requête à l'API de Mistral
try:
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    # Récupérer et afficher la réponse nettoyée
    reponse_nettoyee = chat_response.choices[0].message.content
    print(reponse_nettoyee)

    with open('nouveau_bolivie.txt', 'w', encoding='utf-8') as fichier:
        fichier.write(reponse_nettoyee)
except Exception as e:
    print(f"Une erreur est survenue : {e}")



