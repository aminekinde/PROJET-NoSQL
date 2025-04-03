from queries import *
from database import connect_to_neo4j


# Appel des fonctions
print("Création des noeuds de type Film...")
create_film_nodes()

print("Création des noeuds de type Actor...")
create_actor_nodes()

print("Création des relations ACTED_IN...")
create_film_actor_relation()

print("Création des noeuds pour les membres du projet...")
create_team_nodes_and_attach_to_film()

print("Création des noeuds de type Réalisateur...")
create_director_nodes()

print("Création des relations Directed by...")
create_directed_by_relation()

print("Création des noeuds genres...")
create_genre_nodes()

print("Création des relations has genre by...")
create_film_genre_relation()

print("Toutes les opérations ont été exécutées avec succès !")
