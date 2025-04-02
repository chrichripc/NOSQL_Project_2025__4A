PROJET NoSQL 4A - ESIEA (2024 -2025)

II Objectif
Ce projet a été réalisé dans le cadre du cours de base de données NoSQL en 4A à l’ESIEA.  
Il vise à explorer deux types de bases NoSQL :
- **MongoDB** (base orientée document)
- **Neo4j** (base orientée graphe)

L'application est dévelopée en **Python** avec l'interface **Streamlit** pour faciliter l'interaction et la visualisation.

_____________________________________________

Fonctionnalités de l'application
Interrogation MongoDB

- Rechercher un film par son titre
- Ajouter, mettre à jour et supprimer un film
- Visualisation :
  - Histogramme du nombre de films par année
  - Histogramme des films par genre
  - Corrélation durée ↔ revenu
  - Évolution de la durée moyenne par décennie
- Réponses aux **13 questions du TP MongoDB** directement depuis l’interface

🧠 Intégration Neo4j

- Connexion sécurisée à une instance Neo4j Aura Cloud
- Création automatique du graphe (Films, Acteurs, Réalisateurs, Genres, Relations)
- Lancement manuel depuis l’interface


_______________________________________

Structure du projet 

.
├── app
│   ├── config.py
│   ├── __init__.py
│   ├── main_app.py
│   ├── mongodb_handler.py
│   ├── neo4j_handler.py
│   └── __pycache__
├── data
│   └── movies.json
├── Neo4j-264ab824-Created-2025-04-01.txt
├── rapports_questions.txt
├── request_neo4j.cypher
├── requirements.txt
├── resquest.txt
├── streamlit_app.py
└── venv
    ├── bin
    ├── etc
    ├── include
    ├── lib
    ├── lib64 -> lib
    ├── pyvenv.cfg
    └── share
__________________________________________________________


Technologies utilisées

- [Streamlit](https://streamlit.io/) – Interface web en Python
- [Pymongo](https://pymongo.readthedocs.io/) – Accès MongoDB
- [Neo4j Python Driver](https://neo4j.com/docs/api/python-driver/current/) – Accès Neo4j
- [Matplotlib / Pandas](https://pandas.pydata.org/) – Visualisation des données


Lancer le projet 

python -m venv venv
source venv/bin/activate 

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run streamlit_app.py




