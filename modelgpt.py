#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import logging
import openai
from prettytable import PrettyTable

# Configuration de la journalisation
logging.basicConfig(filename='modelgpt.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fonction pour charger les informations utilisateur depuis le fichier JSON
def load_user_info_from_file(file_path='user_info.json'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_path)
    if not os.path.exists(full_path):
        logging.error(f"Fichier non trouvé : {full_path}")
        raise FileNotFoundError(f"Le fichier {full_path} est introuvable.")
    with open(full_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Fonction pour lister les modèles disponibles de l'API OpenAI
def list_available_models(api_key):
    openai.api_key = api_key
    try:
        # Appel à la nouvelle API pour obtenir la liste des modèles
        response = openai.Model.list()

        # Création d'un tableau pour afficher les résultats
        table = PrettyTable()
        table.field_names = ["Model ID", "Owned By", "Permissions"]

        # Ajout des modèles au tableau
        for model in response['data']:
            model_id = model.get('id', 'N/A')
            owned_by = model.get('owned_by', 'N/A')
            permissions = model.get('permission', 'N/A')  # Vérification de la présence de 'permission'
            
            # Formatage pour éviter l'erreur si 'permissions' est une liste
            if isinstance(permissions, list):
                permissions = ', '.join([perm.get('id', 'N/A') for perm in permissions])
            table.add_row([model_id, owned_by, permissions])

        # Affichage du tableau
        print(table)
        logging.info("Liste des modèles disponibles récupérée et affichée avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des modèles disponibles : {e}")
        print(f"Erreur lors de la récupération des modèles : {e}")

def main():
    try:
        user_info = load_user_info_from_file()

        if not user_info.get("openai_api_key"):
            logging.error("La clé API OpenAI est manquante dans user_info.json.")
            print("Erreur : La clé API OpenAI est manquante dans user_info.json.")
            return

        # Appeler la fonction pour lister les modèles disponibles
        list_available_models(user_info["openai_api_key"])

    except Exception as e:
        logging.error(f"Erreur dans l'exécution du programme : {e}")
        print(f"Erreur dans l'exécution du programme : {e}")

if __name__ == "__main__":
    main()
