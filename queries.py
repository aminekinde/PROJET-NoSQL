from database import connect_to_mongo
import streamlit as st
from bson.objectid import ObjectId
from bson.son import SON
import matplotlib.pyplot as plt
import numpy as np


def get_films(limit=10):
    """
    Récupère une liste de films depuis MongoDB avec une limite spécifiée.
    
    :param limit: Nombre maximum de films à récupérer (par défaut: 10).
    :return: Liste de films sous forme de dictionnaires.
    """
    db = connect_to_mongo()
    films_collection = db.films  # Assure-toi que le nom de la collection est correct
    return list(films_collection.find({}, {"_id": 0}).limit(limit))  # Exclut le champ _id

def insert_film(film_data):
    """
    Insère un nouveau film dans la collection films.
    
    :param film_data: Dictionnaire contenant les informations du film.
    :return: ID du document inséré.
    """
    db = connect_to_mongo()
    result = db.films.insert_one(film_data)
    return result.inserted_id

def update_film(film_id, updated_data):
    """
    Met à jour un film dans la collection films.
    
    :param film_id: ID du film à mettre à jour.
    :param updated_data: Dictionnaire des champs à modifier.
    :return: Résultat de la mise à jour.
    """
    db = connect_to_mongo()
    result = db.films.update_one({"_id": ObjectId(film_id)}, {"$set": updated_data})
    return result.modified_count  # Nombre de documents modifiés

def delete_film(film_id):
    """
    Supprime un film de la collection films.
    
    :param film_id: ID du film à supprimer.
    :return: Résultat de la suppression.
    """
    db = connect_to_mongo()
    result = db.films.delete_one({"_id": ObjectId(film_id)})
    return result.deleted_count  # Nombre de documents supprimés




# Question 1 - Afficher l’année où le plus grand nombre de films ont été sortis
def repondre_question_1():
    """
    Trouver l'année où le plus grand nombre de films ont été sortis.
    """
    films = connect_to_mongo().films
    result = list(films.aggregate([
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1)])},
        {"$limit": 1}
    ]))

    if result:
        year = result[0]['_id']
        count = result[0]['count']
        st.subheader(f"L'année où le plus grand nombre de films ont été sortis est : {year}")
        st.write(f"Nombre de films : {count}")
    else:
        st.warning("Aucun résultat trouvé pour cette question.")

# Question 2 - Nombre de films sortis après l'année 1999
def repondre_question_2():
    """
    Nombre de films sortis après l'année 1999.
    """
    print('Réponse à la question 2 ...')
    films = connect_to_mongo().films
    count = films.count_documents({"year": {"$gt": 1999}})
    print(count)
    return count

# Question 3 - Moyenne des votes des films sortis en 2007
def repondre_question_3():
    """
    Moyenne des votes des films sortis en 2007.
    """
    print('Réponse à la question 3 ...')
    films = connect_to_mongo().films
    result = films.aggregate([
        {"$match": {"year": 2007}},
        {"$group": {"_id": None, "average_votes": {"$avg": "$Votes"}}}
    ])
    return list(result)[0]['average_votes']

# Question 4 - Afficher un histogramme du nombre de films par année
def repondre_question_4():
    """
    Afficher un histogramme du nombre de films par année.
    """
    print('Réponse à la question 4 ...')
    films = connect_to_mongo().films
    data = films.aggregate([
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ])
    years = []
    counts = []
    for item in data:
        years.append(item['_id'])
        counts.append(item['count'])
    
    plt.bar(years, counts)
    plt.xlabel('Année')
    plt.ylabel('Nombre de films')
    plt.title('Nombre de films par année')
    plt.show()

# Question 5 - Genres de films disponibles dans la base
def repondre_question_5():
    """
    Afficher les genres de films disponibles dans la base.
    """
    print('Réponse à la question 5 ...')
    films = connect_to_mongo().films
    genres = films.distinct("genre")
    return genres

# Question 6 - Film ayant généré le plus de revenu
def repondre_question_6():
    """
    Trouver le film ayant généré le plus de revenu.
    """
    print('Réponse à la question 6 ...')
    films = connect_to_mongo().films
    result = films.find_one(sort=[("Revenue", -1)])
    return result['title'], result['Revenue']

# Question 7 - Réalisateurs ayant réalisé plus de 5 films
def repondre_question_7():
    """
    Trouver les réalisateurs ayant réalisé plus de 5 films.
    """
    print('Réponse à la question 7 ...')
    films = connect_to_mongo().films
    result = films.aggregate([
        {"$group": {"_id": "$director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5}}},
        {"$sort": {"count": -1}}
    ])
    return list(result)

# Question 8 - Genre de film qui rapporte en moyenne le plus de revenus
def repondre_question_8():
    """
    Trouver le genre de film qui rapporte en moyenne le plus de revenus.
    """
    print('Réponse à la question 8 ...')
    films = connect_to_mongo().films
    result = films.aggregate([
        {"$group": {"_id": "$genre", "average_revenue": {"$avg": "$Revenue"}}},
        {"$sort": {"average_revenue": -1}},
        {"$limit": 1}
    ])
    return list(result)[0]

# Question 9 - Films les mieux notés pour chaque décennie (1990-1999, 2000-2009, etc.)
def repondre_question_9():
    """
    Trouver les 3 films les mieux notés pour chaque décennie.
    """
    print('Réponse à la question 9 ...')
    films = connect_to_mongo().films
    result = films.aggregate([
        {"$project": {"title": 1, "rating": 1, "decade": {"$floor": {"$divide": ["$year", 10]}}}},
        {"$group": {"_id": "$decade", "films": {"$push": {"title": "$title", "rating": "$rating"}}}},
        {"$unwind": "$films"},
        {"$sort": {"films.rating": -1}},
        {"$group": {"_id": "$_id", "top_films": {"$push": "$films"}}},
        {"$project": {"top_films": {"$slice": ["$top_films", 3]}}}
    ])
    return list(result)

# Question 10 - Film le plus long par genre
def repondre_question_10():
    """
    Trouver le film le plus long par genre.
    """
    print('Réponse à la question 10 ...')
    films = connect_to_mongo().films
    result = films.aggregate([
        {"$group": {"_id": "$genre", "longest_film": {"$max": "$Runtime"}}},
        {"$sort": {"longest_film": -1}},
        {"$limit": 1}
    ])
    return list(result)[0]

# Question 11 - Vue MongoDB des films ayant une note supérieure à 80 et généré plus de 50 millions de dollars
def repondre_question_11():
    """
    Créer une vue MongoDB pour afficher les films ayant une note > 80 et généré plus de 50 millions de dollars.
    """
    print('Réponse à la question 11 ...')
    films = connect_to_mongo().films
    result = films.find({"Metascore": {"$gt": 80}, "Revenue": {"$gt": 50000000}})
    return list(result)

# Question 12 - Corrélation entre la durée des films (Runtime) et leur revenu (Revenue)
def repondre_question_12():
    """
    Calculer la corrélation entre la durée des films (Runtime) et leur revenu (Revenue).
    """
    print('Réponse à la question 12 ...')
    films = connect_to_mongo().films
    data = list(films.find({"Runtime": {"$ne": None}, "Revenue": {"$ne": None}}, {"Runtime": 1, "Revenue": 1}))
    runtimes = [film['Runtime'] for film in data]
    revenues = [film['Revenue'] for film in data]
    
    # Calcul de la corrélation
    correlation = np.corrcoef(runtimes, revenues)[0, 1]
    return correlation

# Question 13 - Évolution de la durée moyenne des films par décennie
def repondre_question_13():
    """
    Analyser l’évolution de la durée moyenne des films par décennie.
    """
    print('Réponse à la question 13 ...')
    films = connect_to_mongo().films
    result = films.aggregate([
        {"$project": {"Runtime": 1, "decade": {"$floor": {"$divide": ["$year", 10]}}}},
        {"$group": {"_id": "$decade", "average_runtime": {"$avg": "$Runtime"}}},
        {"$sort": {"_id": 1}}
    ])
    return list(result)

