import streamlit as st
from queries import *

def main():
    """
    Interface utilisateur principale de l'application Streamlit.
    """
    st.title("Streamlit NoSQL Web App \nAmine KINDE | Computer Science Engineer")  # Titre de l'application
    st.write("Application Web pour la manipulation de bases de donénes NoSQL MongoDB et Neo4j.")  # Description

    # Nombre de films à afficher par page
    limit = st.slider("Nombre de films à afficher", 1, 50, 10)

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

if __name__ == "__main__":
    main()
