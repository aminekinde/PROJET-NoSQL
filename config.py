# config.py
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Charger l'URI MongoDB depuis les variables d'environnement
MONGO_URI = os.getenv("MONGO_URI")
if MONGO_URI is None:
    raise ValueError("L'URI MongoDB n'est pas défini dans les variables d'environnement.")