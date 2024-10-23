# angel
==============================
       Team AVHIRAL 2024
==============================

# Programme Angel Gardien

Ce projet est un service d'automatisation basé sur Python appelé "Angel Gardien" qui interagit avec l'API OpenAI pour générer des scripts pour diverses tâches. Il inclut un rapport quotidien envoyé par e-mail, l'exécution de scripts et la journalisation des actions.

## Présentation :
Le programme Angel Gardien est conçu pour aider à automatiser des tâches telles que la gestion financière, l'amélioration des relations professionnelles et l'automatisation de tâches diverses, en utilisant les modèles de langage OpenAI pour générer des scripts Python basés sur les besoins de l'utilisateur. Il fonctionne en continu en tant que service de fond sur Linux, avec des rapports quotidiens envoyés par e-mail.

## Prérequis :
Pour exécuter le programme Angel Gardien, vous aurez besoin de :
- Un système basé sur Linux (testé sur Ubuntu)
- Python 3.8 ou supérieur
- Pip pour Python 3
- Une clé API OpenAI valide
- Un compte email valide pour envoyer les journaux et les rapports
- Accès à Internet pour l'utilisation de l'API OpenAI

---

## Instructions d'Installation :

### 1. Installation des dépendances requises
Avant d'exécuter le programme, assurez-vous que Python 3, Pip, et les packages nécessaires sont installés :

Ouvrez un terminal et exécutez les commandes suivantes :

```
# Mettre à jour les listes de paquets
sudo apt update

# Installer Python3 et Pip3
sudo apt install python3 python3-pip

# Installer un environnement virtuel Python3 (optionnel)
sudo apt install python3-venv
```

### 2. Installer les packages Python requis
Utilisez `pip3` pour installer les packages requis :

```
# Installer OpenAI (version 0.28.0)
pip3 install openai==0.28.0

# Installer smtplib, cryptography, et autres dépendances
pip3 install cryptography
pip3 install email
```

### 3. Configuration du programme
Téléchargez les fichiers et assurez-vous que la structure du répertoire est la suivante :

```
/root/angel/
    - angel.py
    - email_test.py
    - user_info.json
    - chathpgscriptcrypt.key
    - angel.log
    - angelmail.log
```

### 4. Configuration
- **user_info.json** : Modifiez le fichier `user_info.json` pour inclure votre clé API OpenAI, votre compte email et votre mot de passe. Voici un exemple de configuration :

```
{
    "nom": "Dupond",
    "prenom": "Jean",
    "date_de_naissance": "05/01/1995",
    "lieu_de_naissance": "Paris",
    "adresse_postale": "Rue de la paix",
    "telephone": "+331122334455",
    "linkedin_compte": "https://www.linkedin.com/in/dupond/",
    "email": "dupond@dupond.com",
    "email_logs": "dupond@dupond.com",
    "email_password": "votre_mot_de_passe_email",
    "openai_api_key": "votre_clé_openai"
}
```

### 5. Mise en place du service SystemD
Pour vous assurer que le programme fonctionne en continu en arrière-plan, créez un service SystemD :

```
sudo nano /etc/systemd/system/angel.service
```

Collez le contenu suivant :

```
[Unit]
Description=Angel Service
After=network-online.target
Wants=network-online.target

[Service]
User=root
Group=root
ExecStart=/usr/bin/python3 /root/angel/angel.py
WorkingDirectory=/root/angel
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Ensuite, exécutez les commandes suivantes pour démarrer et activer le service :

```
# Recharger les services systemd
sudo systemctl daemon-reload

# Démarrer le service Angel
sudo systemctl start angel.service

# Activer le service pour qu'il démarre au démarrage
sudo systemctl enable angel.service
```

### 6. Utilisation et journalisation
- Le programme génère des rapports quotidiens et envoie les journaux à l'adresse email configurée dans `user_info.json`.
- Les logs peuvent être vérifiés dans les fichiers `angel.log` pour les activités générales et `angelmail.log` pour les journaux spécifiques aux emails.

---

# Support et Aide
Pour toute question ou assistance concernant l'utilisation du programme, veuillez contacter l'équipe AVHIRAL 2024.

==============================
Merci d'utiliser Angel Gardien
==============================

DON PAYPAL : https://www.paypal.com/donate/?hosted_button_id=EZW7NMLW8YG4W
