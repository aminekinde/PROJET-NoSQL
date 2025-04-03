import streamlit as st
from queries import * 
def afficher_questions_transverses():
    st.subheader("Réponses aux Questions transverses")

    if st.button("Répondre à la question 27"):
        repondre_question_27()

    if st.button("Répondre à la question 28"):
        repondre_question_28()

    if st.button("Répondre à la question 29"):
        repondre_question_29()

    if st.button("Répondre à la question 30"):
        repondre_question_30()
