from pymongo import MongoClient
from py2neo import Graph
from config import *


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

def connect_to_neo4j():
    """
    Etablit la connexion avec la base de données Neo4j en utilisant py2neo.
    Utilise les informations de connexion définies dans le fichier .env.
    """
    try:
        # Connexion avec les informations de connexion
        driver = Graph(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        return driver
        print("Connexion au driver Neo4j réussie")
    except Exception as e:
        print(f"Erreur de connexion à Neo4j : {e}")
        return None