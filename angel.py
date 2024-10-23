#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import smtplib
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai
from cryptography.fernet import Fernet

# Configuration de la journalisation générale
logging.basicConfig(filename='angel.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration spécifique pour la journalisation des emails dans "angelmail.log"
email_logger = logging.getLogger('emailLogger')
email_logger.setLevel(logging.INFO)
email_handler = logging.FileHandler('angelmail.log')
email_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
email_logger.addHandler(email_handler)

# Fonction pour générer une clé de cryptage et la sauvegarder dans un fichier
def generate_and_save_key(key_file='chathpgscriptcrypt.key'):
    try:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        logging.info(f"Clé générée et sauvegardée à l'emplacement : {os.path.abspath(key_file)}")
        return key
    except Exception as e:
        logging.error(f"Erreur lors de la génération de la clé : {e}")
        return None

# Fonction pour charger ou créer une clé de cryptage
def load_or_create_key(file_path='chathpgscriptcrypt.key'):
    if not os.path.exists(file_path):
        logging.info("Clé non trouvée. Génération d'une nouvelle clé.")
        return generate_and_save_key(file_path)
    else:
        with open(file_path, 'rb') as key_file:
            key = key_file.read()
            logging.info(f"Clé chargée depuis : {os.path.abspath(file_path)}")
        return key

# Chargement des informations utilisateur depuis le fichier JSON
def load_user_info_from_file(file_path='user_info.json'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_path)
    if not os.path.exists(full_path):
        logging.error(f"Fichier non trouvé : {full_path}")
        raise FileNotFoundError(f"Le fichier {full_path} est introuvable.")
    with open(full_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Fonction pour interroger ChatGPT et générer des scripts personnalisés
def generate_script_with_chatgpt(task_description, user_info):
    prompt = (
        f"Crée un script Python détaillé pour {user_info['prenom']} {user_info['nom']}, "
        f"un {user_info['activite_professionnelle']} résidant à {user_info['adresse_postale']}. "
        f"Le script doit accomplir la tâche suivante : {task_description}. "
        f"Le but est d'optimiser les résultats dans les domaines financiers, relationnels ou sociaux. "
        f"Le code doit interagir avec des API, automatiser des tâches web et inclure des commentaires clairs."
    )

    try:
        # Configuration de l'API key depuis le fichier JSON
        openai.api_key = user_info["openai_api_key"]

        # Appel correct de l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )

        # Accès à la réponse générée
        script_code = response['choices'][0]['message']['content'].strip()
        logging.info(f"Script généré par ChatGPT pour la tâche: {task_description}")
        return script_code

    except openai.OpenAIError as e:  # Gestion des erreurs OpenAI
        if "quota" in str(e):
            logging.error("Quota dépassé, mise en pause jusqu'à rétablissement.")
            print("Quota dépassé, en attente pour réessayer.")
            while True:
                time.sleep(3600)  # Attente d'une heure avant de réessayer
                try:
                    # Réessayer de générer le script après l'attente
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=800
                    )
                    # Si le quota est restauré, quitter la boucle
                    script_code = response['choices'][0]['message']['content'].strip()
                    logging.info(f"Script généré après rétablissement du quota pour la tâche: {task_description}")
                    return script_code
                except openai.OpenAIError as e:
                    if "quota" not in str(e):
                        logging.error(f"Autre erreur OpenAI : {e}")
                        return None
        else:
            logging.error(f"Erreur OpenAI : {e}")
            return None

    except Exception as e:
        logging.error(f"Erreur lors de la génération du script avec ChatGPT: {e}")
        return None

# Fonction pour envoyer des emails
def send_email(user_info, subject, body):
    sender_email = user_info["email"]
    receiver_email = user_info["email_logs"]
    password = user_info["email_password"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        logging.info("Tentative de connexion au serveur SMTP...")
        email_logger.info("Tentative de connexion au serveur SMTP...")

        with smtplib.SMTP_SSL("serveur.serveur", 465) as server:
            server.login(sender_email, password)
            logging.info(f"Authentification réussie pour l'email {sender_email}")
            email_logger.info(f"Authentification réussie pour l'email {sender_email}")

            # Envoi de l'email
            server.sendmail(sender_email, receiver_email, message.as_string())
            logging.info(f"Email envoyé à {receiver_email} avec le sujet : {subject}")
            email_logger.info(f"Email envoyé à {receiver_email} avec le sujet : {subject}")

    except Exception as e:
        logging.error(f"Échec de l'envoi de l'email à {receiver_email}: {e}")
        email_logger.error(f"Échec de l'envoi de l'email à {receiver_email}: {e}")
        print(f"Erreur lors de l'envoi de l'email : {e}")

# Fonction principale d'automatisation avec gestion du quota
def main():
    try:
        # Charger ou créer la clé de cryptage
        logging.info("Chargement ou création de la clé de cryptage.")
        key = load_or_create_key()
        
        # Charger les informations utilisateur depuis le fichier JSON
        logging.info("Chargement des informations utilisateur.")
        user_info = load_user_info_from_file()

        if not user_info:
            logging.error("Les informations utilisateur sont manquantes.")
            return

        logging.info("Angel Gardien démarré avec succès.")
        print("Angel est lancé et va être votre Ange Gardien.")

        # Génération du rapport quotidien et envoi par email
        logging.info("Génération du rapport quotidien.")
        daily_report(user_info)

    except Exception as e:
        # Capture des erreurs globales dans la fonction principale
        logging.error(f"Erreur dans le processus d'automatisation : {e}")
        print(f"Erreur dans le processus principal : {e}")

    # Mise en pause de 24 heures avant la prochaine exécution
    logging.info("Mise en pause de 24 heures avant la prochaine exécution.")
    time.sleep(86400)

# Génération d'un rapport quotidien
def daily_report(user_info):
    try:
        with open('angel.log', 'r') as log_file:
            log_content = log_file.read()

        report_content = f"""
        Rapport quotidien des actions de votre Ange Gardien :

        - Scripts exécutés pour améliorer les aspects financiers, relationnels, et sociaux.
        - Opportunités découvertes et actions automatisées effectuées.

        Détails du journal d'exécution :

        {log_content}

        Merci d'utiliser Angel Gardien.
        """

        logging.info("Tentative d'envoi du rapport quotidien...")
        email_logger.info("Tentative d'envoi du rapport quotidien...")
        send_email(user_info, "Rapport quotidien", report_content)
    except Exception as e:
        logging.error(f"Erreur lors de la génération du rapport quotidien : {e}")
        email_logger.error(f"Erreur lors de la génération du rapport quotidien : {e}")
        print(f"Erreur dans daily_report : {e}")

if __name__ == "__main__":
    main()