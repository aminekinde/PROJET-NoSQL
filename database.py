import os
from pymongo import MongoClient
from config import MONGO_URI



def connect_to_mongo():
    """
    Etablit la connexion avec la base de données MongoDB en utilisant pymongo.
    Utilise les informations de connexion définies dans le fichier .env.
    """
    try:
        # Connexion avec les informations de connexion
        uri = MONGO_URI
        client = MongoClient(uri)
        db = client['entertainment']
        return db
    except Exception as e:
        print(f"Erreur de connexion à MongoDB : {e}")
        return None
