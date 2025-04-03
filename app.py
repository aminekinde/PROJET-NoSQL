import streamlit as st
from queries import * 
from Page_MongoDB import * 
from Page_Neo4j import *
from Page_Transverse import *

def main():
    """
    Interface utilisateur principale de l'application Streamlit.
    """
    st.title("Streamlit NoSQL Web App \nAmine KINDE | Computer Science Engineer")  # Titre de l'application
    st.write("Application Web pour la manipulation de bases de données NoSQL MongoDB et Neo4j.")  # Description

    # Menu de navigation
    page = st.sidebar.radio("Sélectionner une page", ("Films", "MongoDB","Neo4j","Transeverse"))

    if page == "Films":
        afficher_films()
    elif page == "MongoDB":
        afficher_questions_mongodb()
    elif page == "Neo4j":
        afficher_questions_neo4j()
    elif page == "Transeverse":
        afficher_questions_transverses()

def afficher_films():
    """
    Afficher la liste des films avec un curseur pour limiter le nombre de films à afficher.
    """
    st.subheader("Liste des Films")
    limit = st.slider("Nombre de films à afficher par page", 1, 50, 10)

    if st.button("Afficher les films"):
        try:
            films = get_films(limit)  # Appel de la fonction avec une limite
            if films:
                for film in films:
                    with st.expander(f"🎬 {film['title']} ({film['year']})"):
                        st.write(f"**Genre**: {film['genre']}")
                        st.write(f"**Description**: {film['Description']}")
                        st.write(f"**Note**: {film['rating']} | **Votes**: {film['Votes']}")
            else:
                st.warning("Aucun film trouvé.")
        except Exception as e:
            st.error(f"Erreur lors de la récupération des films: {e}")

    # Boutons pour les opérations CRUD (Insert, Update, Delete)
    st.subheader("Opérations sur les Films")
    
    # Bouton pour insérer un film
    if st.button("Insérer un Film"):
        insert_film_form()  # Afficher le formulaire d'insertion

    # Bouton pour mettre à jour un film
    if st.button("Mettre à jour un Film"):
        update_film_form()  # Afficher le formulaire de mise à jour

    # Bouton pour supprimer un film
    delete_film_form()  # Afficher le formulaire de suppression

def insert_film_form():
    """
    Affiche le formulaire pour insérer un film.
    """
    st.subheader("Insérer un Nouveau Film")
    
    title = st.text_input("Titre du film")
    genre = st.text_input("Genre du film")
    description = st.text_area("Description du film")
    rating = st.number_input("Note du film", min_value=0.0, max_value=10.0, step=0.1)
    votes = st.number_input("Nombre de votes", min_value=0, step=1)
    year = st.number_input("Année de sortie", min_value=1900, max_value=2100, step=1)

    if st.button("Insérer"):
        if title and genre and description:
            film_data = {
                "title": title,
                "genre": genre,
                "Description": description,
                "rating": rating,
                "Votes": votes,
                "year": year
            }
            try:
                film_id = insert_film(film_data)
                st.success(f"Film inséré avec succès ! ID : {film_id}")
            except Exception as e:
                st.error(f"Erreur lors de l'insertion du film: {e}")
        else:
            st.warning("Veuillez remplir tous les champs obligatoires.")

def update_film_form():
    """
    Affiche le formulaire pour mettre à jour un film.
    """
    st.subheader("Mettre à Jour un Film")
    
    film_id = st.text_input("ID du film à mettre à jour")
    title = st.text_input("Nouveau Titre du film")
    genre = st.text_input("Nouveau Genre du film")
    description = st.text_area("Nouvelle Description du film")
    rating = st.number_input("Nouvelle Note du film", min_value=0.0, max_value=10.0, step=0.1)
    votes = st.number_input("Nouveau Nombre de votes", min_value=0, step=1)
    year = st.number_input("Nouvelle Année de sortie", min_value=1900, max_value=2100, step=1)

    if st.button("Mettre à jour"):
        if film_id:
            updated_data = {
                "title": title,
                "genre": genre,
                "Description": description,
                "rating": rating,
                "Votes": votes,
                "year": year
            }
            try:
                updated_count = update_film(film_id, updated_data)
                if updated_count > 0:
                    st.success(f"{updated_count} film(s) mis à jour avec succès.")
                else:
                    st.warning("Aucun film trouvé avec cet ID.")
            except Exception as e:
                st.error(f"Erreur lors de la mise à jour du film: {e}")
        else:
            st.warning("Veuillez entrer un ID valide.")

def delete_film_form():
    """Affiche le formulaire pour supprimer un film."""
    # Utilisation d'une clé unique pour le champ input pour éviter les conflits
    film_id = st.text_input(f"**Supprimer un film**",key="film_id_input",placeholder ="Id du film à supprimer")
    
    # Bouton unique pour déclencher l'action
    if st.button("Supprimer le film"):
        delete_film(film_id)






if __name__ == "__main__":
    main()
