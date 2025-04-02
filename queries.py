from database import connect_to_mongo
db = connect_to_mongo()

def get_films(limit=10):
    """
    Récupère une liste de films depuis MongoDB avec une limite spécifiée.
    
    :param limit: Nombre maximum de films à récupérer (par défaut: 10).
    :return: Liste de films sous forme de dictionnaires.
    """
    db = connect_to_mongo()
    films_collection = db.films  # Assure-toi que le nom de la collection est correct
    return list(films_collection.find({}, {"_id": 0}).limit(limit))  # Exclut le champ _id

