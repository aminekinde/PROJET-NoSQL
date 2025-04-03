from database import connect_to_mongo
import streamlit as st
from bson.objectid import ObjectId
from bson.son import SON
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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

def find_film_by_id(film_id):
    # Connexion à la collection "films"
    films = connect_to_mongo().films
    # Recherche du film avec find_one
    film = films.find_one({"_id": film_id})
    return film

def delete_film(film_id):
    """
    Supprime un film de la collection films.

    :param film_id: ID du film à supprimer.
    :return: Message indiquant le résultat de la suppression.
    """
    try:
        # Connexion à la collection "films"
        films = connect_to_mongo().films
        film_to_delete = find_film_by_id(film_id)
        if film_to_delete is None:
            st.warning("Film non trouvé. Veuillez entrer un Id de film valide.")
        else :
            # Suppression du film
            films.delete_one({"_id": film_id})
            # Retourner un message de succès
            st.success(f"Le film {film_id} a été supprimé avec succès.")
    except Exception as e:
        # En cas d'erreur, retourner un message approprié
        return f"Une erreur s'est produite : {str(e)}"





# Question 1 - Afficher l’année où le plus grand nombre de films ont été sortis
def repondre_question_1():
    films = connect_to_mongo().films
    result = list(films.aggregate([
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1)])},
        {"$limit": 1}
    ]))
    st.write(f"L'année où le plus grand nombre de films ont été sortis est {result[0]['_id']} avec {result[0]['count']} films")

# Question 2 - Nombre de films sortis après l'année 1999
def repondre_question_2():
    films = connect_to_mongo().films
    count = films.count_documents({"year": {"$gt": 1999}})
    st.write(f"Nombre de films sortis après 1999 est {count}")

# Question 3 - Moyenne des votes des films sortis en 2007
def repondre_question_3():
    films = connect_to_mongo().films
    result = films.aggregate([
        {"$match": {"year": 2007}},
        {"$group": {"_id": None, "average_votes": {"$avg": "$Votes"}}}
    ])
    st.write(f"La Moyenne des votes des films sortis en 2007 est {list(result)[0]['average_votes']}")

# Question 4 - Afficher un histogramme du nombre de films par année
def repondre_question_4():
    films = connect_to_mongo().films
    data = films.aggregate([
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ])
    years = []
    counts = []
    for item in data:
        if item['_id'] is not None:
            years.append(item['_id'])
            counts.append(item['count'])
    
    fig, ax = plt.subplots(figsize=(10, 5))  # Créer une figure et un axe
    ax.bar(years, counts)  # Utiliser ax pour tracer le graphique
    ax.set_xlabel('Année')
    ax.set_ylabel('Nombre de films')
    ax.set_title('Nombre de films par année')

    st.pyplot(fig)  # Passer la figure à st.pyplot()


# Question 5 - Genres de films disponibles dans la base
def repondre_question_5():
    films = connect_to_mongo().films

    # Agrégation pour split et unwind les genres, puis utiliser $group pour obtenir les genres distincts
    data = films.aggregate([
        {"$project": {"genres": {"$split": ["$genre", ","]}}},  # Split genres en tableau
        {"$unwind": "$genres"},  # Décompose chaque genre en un document séparé
        {"$group": {"_id": "$genres"}},  # Regroupe par genre pour obtenir les genres distincts
        {"$sort": {"_id": 1}}  # Tri par ordre alphabétique croissant
    ])

    # Extraire les genres distincts
    genres_distincts = [item["_id"] for item in data]

    # Affichage des genres
    st.write(f"Les genres disponibles dans la base sont {', '.join(genres_distincts)}")


    

# Question 6 - Film ayant généré le plus de revenu
def repondre_question_6():
    films = connect_to_mongo().films
    result = films.find_one(
    {"Revenue (Millions)": {"$ne": ""}},  # Exclure les films avec un revenu vide
    sort=[("Revenue (Millions)", -1)]  # Trier par revenu décroissant
)
    st.write(f"Le film ayant généré le plus de revenu est  {result['title']} avec {result["Revenue (Millions)"]} millions de dollars")

# Question 7 - Réalisateurs ayant réalisé plus de 5 films
def repondre_question_7():
    films = connect_to_mongo().films
    result = list(films.aggregate([
        {"$group": {"_id": "$Director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5}}},
        {"$sort": {"count": -1}}
    ]))
    if len(result)  == 0:
        st.write("Aucun réalisateur n'a réalisé plus de 5 films.")
    else:
        st.write(f"Réalisateurs ayant réalisé plus de 5 films :")
        for r in result:
            st.write(f"- {r['_id']} : {r['count']} films")

# Question 8 - Genre de film qui rapporte en moyenne le plus de revenus
def repondre_question_8():
    films = connect_to_mongo().films
    result = list(films.aggregate([
        {"$group": {"_id": "$genre", "average_revenue": {"$avg": "$Revenue (Millions)"}}},
        {"$sort": {"average_revenue": -1}},
        {"$limit": 1}
    ]))
    st.write(f"Le genre de film qui rapporte en moyenne le plus de revenus est  {result[0]['_id']} avec une moyenne de {result[0]['average_revenue']} millions de dollars")

# Question 9 - Films les mieux notés pour chaque décennie
def repondre_question_9():
    films = connect_to_mongo().films
    result = list(films.aggregate([
        {"$match": {"rating": {"$ne": "unrated"}}},  # Exclure les films "unrated"
        {"$project": {
            "title": 1, 
            "decade": {"$floor": {"$divide": ["$year", 10]}}}
        },
        {"$group": {
            "_id": "$decade", 
            "films": {"$push": {"title": "$title"}}}
        },
        {"$unwind": "$films"},
        {"$sort": {"films.title": 1}},  # Trier par titre
        {"$group": {
            "_id": "$_id", 
            "top_films": {"$push": "$films"}}
        },
        {"$project": {
            "top_films": {"$slice": ["$top_films", 3]}  # Garder les 3 meilleurs films
        }}
    ]))
    
    # Afficher le résultat : Décennie et Titres des films
    for decade in result:
        st.write(f"Décennie: {decade['_id'] * 10}s")
        for film in decade['top_films']:
            st.write(f"- {film['title']}")



# Question 10 - Film le plus long par genre
def repondre_question_10():
    films = connect_to_mongo().films
    result = list(films.aggregate([
        {"$match": {"Runtime (Minutes)": {"$exists": True}}},  # S'assurer que la durée existe
        {"$project": {
            "genre": 1,
            "title": 1,
            "Runtime (Minutes)": 1
        }},
        {"$group": {
            "_id": "$genre", 
            "films": {"$push": {"title": "$title", "Runtime (Minutes)": "$Runtime (Minutes)"}}
        }},
        {"$unwind": "$films"},
        {"$sort": {"films.Runtime (Minutes)": -1}}  # Trier par durée décroissante
    ]))

    # Afficher le résultat : Genre, Titre et Durée du film
    for genre in result:
        st.write(f"Genre: {genre['_id']}")
        st.write(f"- Titre: {genre['films']['title']}, Durée: {genre['films']['Runtime (Minutes)']} minutes")




# Question 11 - Vue MongoDB des films ayant une note supérieure à 80 et généré plus de 50 millions de dollars
def repondre_question_11():
    films = connect_to_mongo().films
    result = list(films.find(
        {"Metascore": {"$gt": 80}, "Revenue (Millions)": {"$gt": 50}},
        {"title": 1, "Metascore": 1, "Revenue (Millions)": 1, "_id": 0}  # Projeter uniquement title, Metascore et Revenue
    ))
    st.write("Films ayant une note > 80 et généré plus de 50 millions de dollars :")
    for film in result:
        st.write(f"- Titre: {film['title']}, Score: {film['Metascore']}, Revenu: {film['Revenue (Millions)']} millions de dollars")


# Question 12 - Corrélation entre la durée des films (Runtime) et leur revenu (Revenue)
def repondre_question_12():
    films = connect_to_mongo().films
    data = list(films.find({"Runtime (Minutes)": {"$ne": None}, "Revenue (Millions)": {"$ne": ''}}, {"Runtime (Minutes)": 1, "Revenue (Millions)": 1}))
    runtimes = [film['Runtime (Minutes)'] for film in data]
    revenues = [film['Revenue (Millions)'] for film in data]

    correlation = round(np.corrcoef(runtimes, revenues)[0, 1],2)*100
    st.write(f"La corrélation entre la durée des films et leur revenu est de {correlation}%")

# Question 13 - Évolution de la durée moyenne des films par décennie
def repondre_question_13():
    films = connect_to_mongo().films
    result = films.aggregate([
        {"$project": {"Runtime (Minutes)": 1, "decade": {"$floor": {"$divide": ["$year", 10]}}}},
        {"$group": {"_id": "$decade", "average_runtime": {"$avg": "$Runtime (Minutes)"}}},
        {"$sort": {"_id": 1}}
    ])

    # Convertir les données en DataFrame
    data = [{"decade": int(entry["_id"]) * 10, "average_runtime": entry["average_runtime"]} for entry in result]
    df = pd.DataFrame(data)

    # Création du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(df["decade"], df["average_runtime"], marker='o', linestyle='-', color='b')

    # Ajouter des étiquettes de données pour chaque point
    for i, row in df.iterrows():
        plt.text(row["decade"], row["average_runtime"], f'{row["average_runtime"]:.2f}', 
                 ha='center', va='bottom', fontsize=9, color='black')

    # Ajouter les titres et les labels
    plt.title("Évolution de la durée moyenne des films par décennie", fontsize=14)
    plt.xlabel("Décennie", fontsize=12)
    plt.ylabel("Durée Moyenne (Minutes)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(df["decade"], rotation=45)  # Rotation des labels des décennies pour plus de lisibilité

    # Afficher le graphique dans Streamlit
    st.pyplot(plt)
