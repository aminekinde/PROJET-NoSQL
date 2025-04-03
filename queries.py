from database import *
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

###################### NEO4J ###################### 

# Connexion à Neo4j
driver = connect_to_neo4j()

# Connexion à MongoDB
films_collection = connect_to_mongo().films

### 1. Créer des noeuds de type Film ###
def create_film_nodes():
    """
    Créer des noeuds de type Film contenant uniquement les champs _id, title, year, Votes,
    Revenue (Millions), rating et director.
    """
    films = films_collection.find()
    for film in films:
        driver.run("""
        MERGE (:Film {
            _id: $id,
            title: $title,
            year: $year,
            Votes: $votes,
            Revenue: $revenue,
            rating: $rating,
            director: $director
        })
        """, id=film["_id"],
        title=film.get("title", ""),
        year=film.get("year", None),
        votes=film.get("Votes", None),
        revenue=film.get("Revenue (Millions)", None),
        rating=film.get("rating", None),
        director=film.get("Director", ""))
    print("Nœuds de type Film créés avec succès !")


### 2. Créer des noeuds de type Actor ###
def create_actor_nodes():
    """
    Créer des nœuds de type Actor contenant uniquement les acteurs de manière distincte.
    """
    films = films_collection.find()
    actors_set = set()  # Pour éviter les doublons
    for film in films:
        actors = film.get("Actors", "").split(",") if film.get("Actors") else []
        for actor in actors:
            actors_set.add(actor.strip())
    
    for actor in actors_set:
        driver.run("""
        MERGE (:Actor {name: $name})
        """, name=actor)
    print("Nœuds de type Actor créés avec succès !")


### 3. Créer des relations 'A joué' ###
def create_film_actor_relation():
    """
    Créer des relations 'ACTED_IN' entre les acteurs et les films dans lesquels ils ont joué.
    """
    films = films_collection.find()
    for film in films:
        actors = film.get("Actors", "").split(",") if film.get("Actors") else []
        for actor in actors:
            driver.run("""
            MATCH (f:Film {_id: $id})
            MERGE (a:Actor {name: $name})
            MERGE (a)-[:ACTED_IN]->(f)
            """, id=film["_id"], name=actor.strip())
    print("Relations 'ACTED_IN' créées avec succès !")


### 4. Créer des nœuds pour les membres du projet ###
def create_team_nodes_and_attach_to_film():
    """
    Créer des nœuds pour les membres du projet et les relier à un film spécifique.
    """
    team_members = ["Amine", "Alex", "Marie", "Sophie"]  # Membres du projet
    film_title = "Inception"  # Film de mon choix

    for member in team_members:
        driver.run("""
        MERGE (m:Actor {name: $name})
        WITH m
        MATCH (f:Film {title: $film})
        MERGE (m)-[:CONTRIBUTED_TO]->(f)
        """, name=member, film=film_title)
    print("Nœuds pour les membres du projet créés et liés à un film avec succès !")


### 5. Créer des noeuds pour les Réalisateurs ###
def create_director_nodes():
    """
    Créer des nœuds de type Réalisateur depuis le champ Director de la base MongoDB.
    """
    films = films_collection.find()
    directors_set = set()  # Pour éviter les doublons
    for film in films:
        director = film.get("Director", "").strip()
        if director:
            directors_set.add(director)
    
    for director in directors_set:
        driver.run("""
        MERGE (:Director {name: $name})
        """, name=director)
    print("Nœuds de type Réalisateur créés avec succès !")

### 6. Créer la relation 'DIRECTED_BY' ###
def create_directed_by_relation():
    """
    Créer des relations 'DIRECTED_BY' entre les réalisateurs et les films qu'ils ont réalisés.
    """
    films = films_collection.find()
    for film in films:
        director = film.get("Director", "").strip()
        if director:
            driver.run("""
            MATCH (f:Film {_id: $id})
            MERGE (d:Director {name: $name})
            MERGE (d)-[:DIRECTED_BY]->(f)
            """, id=film["_id"], name=director)
    print("Relations 'DIRECTED_BY' créées avec succès !")

### 7. Création du noeud genre
def create_genre_nodes():
    """
    Créer des nœuds de type Genre contenant uniquement les genres distincts présents dans les films.
    """
    films = films_collection.find()
    genres_set = set()  # Pour éviter les doublons
    for film in films:
        genres = film.get("genre", "").split(",") if film.get("genre") else []
        for genre in genres:
            genres_set.add(genre.strip())
    
    for genre in genres_set:
        driver.run("""
        MERGE (:Genre {name: $name})
        """, name=genre)
    print("Nœuds de type Genre créés avec succès !")

def create_film_genre_relation():
    """
    Créer des relations 'HAS_GENRE' entre les films et les genres dans lesquels ils appartiennent.
    """
    films = films_collection.find()
    for film in films:
        genres = film.get("genre", "").split(",") if film.get("genre") else []
        for genre in genres:
            driver.run("""
            MATCH (f:Film {_id: $id})
            MERGE (g:Genre {name: $genre})
            MERGE (f)-[:HAS_GENRE]->(g)
            """, id=film["_id"], genre=genre.strip())
    print("Relations 'HAS_GENRE' créées avec succès !")


import streamlit as st
from database import connect_to_neo4j

driver = connect_to_neo4j()

### 14. Acteur ayant joué dans le plus grand nombre de films ###
def repondre_question_14():
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
    RETURN a.name AS Acteur, COUNT(f) AS NombreDeFilms
    ORDER BY NombreDeFilms DESC
    LIMIT 1
    """
    result = driver.run(query).data()
    if result:
        acteur, nb_films = result[0]["Acteur"], result[0]["NombreDeFilms"]
        st.write(f"🎭 L'acteur ayant joué dans le plus grand nombre de films est **{acteur}** avec **{nb_films}** films.")
    else:
        st.write("Aucun résultat trouvé.")

### 15. Acteurs ayant joué avec Anne Hathaway ###
def repondre_question_15():
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)<-[:ACTED_IN]-(anne:Actor {name: "Anne Hathaway"})
    RETURN DISTINCT a.name AS Acteur
    """
    result = driver.run(query).data()
    acteurs = [r["Acteur"] for r in result]
    st.write(f"🎭 Acteurs ayant joué avec Anne Hathaway : {', '.join(acteurs) if acteurs else 'Aucun trouvé.'}")

### 16. Acteur ayant joué dans les films totalisant le plus de revenus ###
def repondre_question_16():
    """
    Trouver l'acteur ayant joué dans des films totalisant le plus de revenus.
    """
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)
    WITH a, SUM(COALESCE(toFloat(f.Revenue), 0)) AS total_revenue
    RETURN a.name AS actor, total_revenue
    ORDER BY total_revenue DESC
    LIMIT 1
    """
    result = driver.run(query).data()
    if result:
        st.write(f"💰 L'acteur ayant joué dans des films totalisant le plus de revenus est : {result[0]['actor']} avec un revenu total de {result[0]['total_revenue']} millions.")
    else:
        st.write("Aucun résultat trouvé pour cette question.")


### 17. Moyenne des votes ###
def repondre_question_17():
    query = """
    MATCH (f:Film)
    RETURN AVG(f.Votes) AS MoyenneVotes
    """
    result = driver.run(query).data()
    moyenne = result[0]["MoyenneVotes"] if result else "N/A"
    st.write(f"⭐ La moyenne des votes est **{moyenne}**.")

### 18. Genre le plus représenté ###
def repondre_question_18():
    """
    Trouver le genre le plus représenté dans la base de données.
    """
    query = """
    MATCH (g:Genre)<-[:HAS_GENRE]-(f:Film)
    RETURN g.name AS genre, COUNT(f) AS genre_count
    ORDER BY genre_count DESC
    LIMIT 1
    """
    result = driver.run(query).data()
    if result:
        st.write(f"🎬 Le genre le plus représenté dans la base de données est : {result[0]['genre']} avec {result[0]['genre_count']} films.")
    else:
        st.write("Aucun genre trouvé dans les films.")


### 19. Films où les acteurs ayant joué avec vous ont également joué ###
def repondre_question_19():
    query = """
    MATCH (me:Actor {name: "Amine"})-[:ACTED_IN]->(f1:Film)<-[:ACTED_IN]-(a:Actor),
          (a)-[:ACTED_IN]->(f2:Film)
    WHERE f1 <> f2
    RETURN DISTINCT f2.title AS Films
    """
    result = driver.run(query).data()
    print(result)
    # films = [r["Films"] for r in result]
    # st.write(f"🎥 Films suggérés : {', '.join(films) if films else 'Aucun trouvé.'}")

### 20. Réalisateur ayant travaillé avec le plus d’acteurs distincts ###
def repondre_question_20():
    query = """
    MATCH (d:Director)<-[:DIRECTED_BY]-(f:Film)<-[:ACTED_IN]-(a:Actor)
    RETURN d.name AS Directeur, COUNT(DISTINCT a) AS NombreActeurs
    ORDER BY NombreActeurs DESC
    LIMIT 1
    """
    result = driver.run(query).data()
    if result:
        directeur, nb_acteurs = result[0]["Directeur"], result[0]["NombreActeurs"]
        st.write(f"🎬 Le réalisateur ayant travaillé avec le plus d’acteurs est **{directeur}** avec **{nb_acteurs}** acteurs.")
    else:
        st.write("Aucun résultat trouvé.")

### 21. Films les plus connectés ###
def repondre_question_21():
    query = """
    MATCH (f1:Film)<-[:ACTED_IN]-(a:Actor)-[:ACTED_IN]->(f2:Film)
    WHERE f1 <> f2
    RETURN f1.title AS Film1, f2.title AS Film2, COUNT(a) AS NombreActeursCommuns
    ORDER BY NombreActeursCommuns DESC
    LIMIT 5
    """
    result = driver.run(query).data()
    if result:
        st.write("🔗 **Films les plus connectés** :")
        for row in result:
            st.write(f"- **{row['Film1']}** ↔ **{row['Film2']}** ({row['NombreActeursCommuns']} acteurs en commun)")
    else:
        st.write("Aucun résultat trouvé.")

### 22. Top 5 des acteurs ayant travaillé avec le plus de réalisateurs ###
def repondre_question_22():
    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(f:Film)-[:DIRECTED_BY]->(d:Director)
    RETURN a.name AS Acteur, COUNT(DISTINCT d) AS NombreDeRealisateurs
    ORDER BY NombreDeRealisateurs DESC
    LIMIT 5
    """
    result = driver.run(query).data()
    st.write("🎭 **Top 5 des acteurs ayant travaillé avec le plus de réalisateurs** :")
    for row in result:
        st.write(f"- {row['Acteur']} : {row['NombreDeRealisateurs']} réalisateurs")

### 23. Recommandation de film à un acteur ###
def repondre_question_23():
    query = """
    MATCH (a:Actor {name: "TonNom"})-[:ACTED_IN]->(f:Film)
    UNWIND split(f.genre, ",") AS GenrePrefere
    MATCH (f2:Film)
    WHERE NOT EXISTS {(a)-[:ACTED_IN]->(f2)}
    AND f2.genre CONTAINS GenrePrefere
    RETURN DISTINCT f2.title AS FilmRecommande, f2.genre AS Genres
    LIMIT 5
    """
    result = driver.run(query).data()
    st.write("🎬 **Films recommandés** :")
    for row in result:
        st.write(f"- {row['FilmRecommande']} ({row['Genres']})")

### 24. Relations d'influence entre réalisateurs ###
def repondre_question_24():
    query = """
    MATCH (d1:Director)-[:DIRECTED_BY]-(f1:Film),
          (d2:Director)-[:DIRECTED_BY]-(f2:Film)
    WHERE d1 <> d2 AND f1.genre = f2.genre
    MERGE (d1)-[:INFLUENCED_BY]->(d2)
    """
    driver.run(query)
    st.write("🔄 Relations **INFLUENCED_BY** ajoutées entre réalisateurs.")

### 25. Chemin le plus court entre acteurs ###
def repondre_question_25():
    query = """
    MATCH p=shortestPath((a1:Actor {name: "Tom Hanks"})-[:ACTED_IN*]-(a2:Actor {name: "Scarlett Johansson"}))
    RETURN p
    """
    result = driver.run(query).data()
    
    if result:
        # Récupérer le chemin du résultat
        path = result[0]["p"]
        
        # Extraire les acteurs et films du chemin
        actors = []
        films = []
        for i in range(0, len(path.nodes) - 1, 2):  # Les nœuds sont alternés entre acteurs et films
            actor = path.nodes[i]
            film = path.nodes[i + 1]
            actors.append(actor['name'])
            films.append(film['title'])
        
        # Créer un affichage formaté
        chemin = " -> ".join([f"{actor} (Film: {film})" for actor, film in zip(actors, films)])
        
        # Afficher le résultat
        st.write(f"🔗 **Chemin le plus court entre Tom Hanks et Scarlett Johansson** :")
        st.write(f"{chemin}")
    else:
        st.write("Aucun chemin trouvé entre Tom Hanks et Scarlett Johansson.")


### 26. Analyse des communautés d'acteurs ###
def repondre_question_26():
    query = """
    CALL gds.graph.create('actorGraph', 
        'Actor', 
        'ACTED_IN', 
        {
            nodeProperties: ['name']
        }
    )
    YIELD graphName, nodeCount, relationshipCount;

    CALL gds.louvain.stream('actorGraph')
    YIELD nodeId, communityId, score
    RETURN gds.util.asNode(nodeId).name AS actor, communityId
    ORDER BY communityId, score DESC
    """
    
    result = driver.run(query).data()
    
    if result:
        st.write("🔍 **Communautés d'acteurs détectées :**")
        for row in result:
            st.write(f"🎭 Acteur : {row['actor']} appartient à la communauté {row['communityId']}")
    else:
        st.write("Aucune communauté détectée.")

def repondre_question_27():
    query = """
    MATCH (f1:Film)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(f2:Film)
    WHERE f1.director <> f2.director
    RETURN f1.title AS Film1, f2.title AS Film2, g.name AS Genre
    ORDER BY Genre
    """
    result = driver.run(query).data()
    if result:
        st.write("🎬 Films ayant des genres en commun mais réalisés par des réalisateurs différents :")
        for row in result:
            st.write(f"🎥 **{row['Film1']}** et **{row['Film2']}** partagent le genre **{row['Genre']}**.")
    else:
        st.write("Aucun film trouvé.")

def repondre_question_28():
    actor_name = "Tom Hanks"  
    query = f"""
    MATCH (a:Actor {{name: '{actor_name}'}})-[:ACTED_IN]->(f:Film)-[:HAS_GENRE]->(g:Genre)
    WITH g, collect(f) AS films
    UNWIND films AS film
    MATCH (f2:Film)-[:HAS_GENRE]->(g)
    WHERE NOT (f2)-[:ACTED_IN]->(:Actor {{name: '{actor_name}'}})
    RETURN f2.title AS RecommendedFilm, g.name AS Genre
    ORDER BY RecommendedFilm
    LIMIT 5
    """
    result = driver.run(query).data()
    if result:
        st.write(f"🎬 Films recommandés pour **{actor_name}** en fonction des genres qu'il a joué :")
        for row in result:
            st.write(f"🎥 **{row['RecommendedFilm']}** (Genre: {row['Genre']})")
    else:
        st.write(f"Aucune recommandation pour {actor_name}.")

def repondre_question_29():
    query = """
    MATCH (d1:Director)-[:DIRECTED_BY]->(f1:Film)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(f2:Film)<-[:DIRECTED_BY]-(d2:Director)
    WHERE d1 <> d2 AND f1.year = f2.year
    MERGE (d1)-[:COMPETES_WITH]->(d2)
    RETURN d1.name AS Director1, d2.name AS Director2, f1.year AS Year
    """
    result = driver.run(query).data()
    if result:
        st.write("🎬 Relations de concurrence entre réalisateurs ayant réalisé des films similaires la même année :")
        for row in result:
            st.write(f"🎥 **{row['Director1']}** et **{row['Director2']}** ont réalisé des films similaires en **{row['Year']}**.")
    else:
        st.write("Aucune concurrence détectée.")


def repondre_question_30():
    query = """
    MATCH (d:Director)-[:DIRECTED_BY]->(f:Film)-[:ACTED_IN]->(a:Actor)
    WITH d.name AS Director, a.name AS Actor, COUNT(f) AS CollaborationCount, AVG(f.revenue) AS AverageRevenue, AVG(f.rating) AS AverageRating
    RETURN Director, Actor, CollaborationCount, AverageRevenue, AverageRating
    ORDER BY CollaborationCount DESC
    LIMIT 5
    """
    result = driver.run(query).data()
    if result:
        st.write("🎬 Collaborations les plus fréquentes entre réalisateurs et acteurs :")
        for row in result:
            st.write(f"🎥 **{row['Director']}** et **{row['Actor']}** ont collaboré **{row['CollaborationCount']}** fois. Revenus moyens : {row['AverageRevenue']}, Note moyenne : {row['AverageRating']}")
    else:
        st.write("Aucune collaboration fréquente trouvée.")
