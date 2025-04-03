import json
import csv

def json_to_csv(file):
    """
    Cette fonction prend un fichier JSON et le convertit en un fichier CSV
    avec les mêmes noms de champs et structure.
    
    :param file: chemin vers le fichier JSON à convertir
    :return: None, crée un fichier CSV dans le même répertoire
    """
    
    films = []
    with open(file, 'r', encoding='utf-8') as json_file:
        # Lire chaque ligne et convertir en objet JSON
        for line in json_file:
            try:
                films.append(json.loads(line))  # Charger chaque ligne comme un objet JSON
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON sur la ligne : {line} - {str(e)}")
    
    # Définir les champs du CSV
    fieldnames = ['_id', 'title', 'genre', 'Description', 'Director', 'Actors', 
                  'year', 'Runtime (Minutes)', 'rating', 'Votes', 'Revenue (Millions)', 'Metascore']
    
    # Créer et écrire dans un fichier CSV
    with open('films.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Écrire l'en-tête du CSV
        writer.writeheader()

        # Écrire les données dans le fichier CSV
        for film in films:
            writer.writerow({
                '_id': film.get('_id', ''),
                'title': film.get('title', ''),
                'genre': film.get('genre', ''),
                'Description': film.get('Description', ''),
                'Director': film.get('Director', ''),
                'Actors': film.get('Actors', ''),
                'year': film.get('year', ''),
                'Runtime (Minutes)': film.get('Runtime (Minutes)', ''),
                'rating': film.get('rating', ''),
                'Votes': film.get('Votes', ''),
                'Revenue (Millions)': film.get('Revenue (Millions)', ''),
                'Metascore': film.get('Metascore', '')
            })
    
    print("Conversion en CSV terminée, fichier 'films.csv' créé.")

# Exemple d'appel de la fonction avec un fichier JSON
json_to_csv('films.json')
