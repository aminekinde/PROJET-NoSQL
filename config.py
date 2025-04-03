# config.py
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Charger l'URI MongoDB depuis les variables d'environnement
MONGO_URI = os.getenv("MONGO_URI")

NEO4J_URI=os.getenv("NEO4J_URI")
NEO4J_USERNAME=os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD=os.getenv("NEO4J_PASSWORD")
AURA_INSTANCEID=os.getenv("AURA_INSTANCEID")
AURA_INSTANCENAME=os.getenv("AURA_INSTANCENAME")