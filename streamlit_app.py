# Interface utilisateur streamlit, interface créee avec l'aide d'internet

import streamlit as st
from app.mongodb_handler import getcollection
from app.neo4j_handler import graph_create_mongo
from neo4j import GraphDatabase
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from bson.objectid import ObjectId
import pandas as pd
import matplotlib.pyplot as plt


# Titre de l'application
st.title("TP NoSQL - 4A ESIEA")
st.subheader("MongoDB & Neo4j - Exploration des données")

# Sélection de la section à afficher
menu = st.sidebar.selectbox("Navigation", ["MongoDB", "Neo4j"])
collection = getcollection()
# Section MongoDB
if menu == "MongoDB":
    st.header(" Interrogation MongoDB")
    

    # 🔍 Recherche par titre
    st.subheader("🔍 Rechercher un film")
    search_title = st.text_input("Titre du film")
    if search_title:
        results = list(collection.find({"title": {"$regex": search_title, "$options": "i"}}))
        if results:
            st.success(f"{len(results)} film(s) trouvé(s) :")
            for film in results:
                st.markdown(f"- **{film.get('title')}** ({film.get('year', '?')})")
        else:
            st.warning("Aucun film trouvé.")

    st.markdown("---")

    # ➕ Ajouter un nouveau film
    st.subheader("➕ Ajouter un film manuellement")

    with st.form("add_film_form"):
        new_title = st.text_input("Titre")
        new_year = st.number_input("Année", min_value=1900, max_value=2100, value=2025)
        new_director = st.text_input("Réalisateur")
        new_genre = st.text_input("Genres (séparés par des virgules)")
        submitted = st.form_submit_button("Ajouter le film")

        if submitted and new_title:
            doc = {
                "title": new_title,
                "year": int(new_year),
                "Director": new_director,
                "genre": new_genre
            }
            collection.insert_one(doc)
            st.success(f"🎬 Film ajouté : {new_title}")

    st.markdown("---")

    # 🗑️ Supprimer un film par ID
    st.subheader("🗑️ Supprimer un film")
    delete_id = st.text_input("ID Mongo (_id)")
    if st.button("Supprimer"):
        try:
            result = collection.delete_one({"_id": ObjectId(delete_id)})
            if result.deleted_count:
                st.success("Film supprimé avec succès.")
            else:
                st.warning("Aucun film trouvé avec cet ID.")
        except Exception as e:
            st.error(f"Erreur : {e}")

    st.markdown("---")
    st.subheader("✏️ Mettre à jour un film (titre + champ)")

    update_id = st.text_input("ID du film à modifier")
    update_field = st.selectbox("Champ à modifier", ["title", "year", "Director", "genre"])
    new_value = st.text_input("Nouvelle valeur")

    if st.button("Mettre à jour"):
        if update_id and update_field and new_value:
            try:
                result = collection.update_one(
                    {"_id": ObjectId(update_id)},
                    {"$set": {update_field: new_value}}
                )
                if result.modified_count:
                    st.success("Film mis à jour avec succès.")
                else:
                    st.warning("Aucune mise à jour effectuée.")
            except Exception as e:
                st.error(f"Erreur : {e}")  
                
    st.markdown("---")
    st.header("Questions )")

    # Q1 - Année avec le plus grand nombre de films
    if st.button("Année avec le plus de films"):
        pipeline = [
            {"$group": {"_id": "$year", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        result = list(collection.aggregate(pipeline))
        st.write("Année la plus prolifique :", result[0]["_id"], f"({result[0]['count']} films)")

    # Q2 - Nombre de films après 1999
    if st.button("Nombre de films après 1999"):
        count = collection.count_documents({"year": {"$gt": 1999}})
        st.write("🎞️ Nombre de films sortis après 1999 :", count)

    # Q3 - Moyenne des votes des films de 2007
    if st.button("Moyenne des votes (2007)"):
        pipeline = [
            {"$match": {"year": 2007}},
            {"$group": {"_id": None, "avg_votes": {"$avg": "$Votes"}}}
        ]
        result = list(collection.aggregate(pipeline))
        moyenne = round(result[0]['avg_votes'], 2) if result else "Non disponible"
        st.write("📊 Moyenne des votes en 2007 :", moyenne)

    # Q4 - Histogramme déjà fait plus haut (donc pas redondant ici)

    # Q5 - Genres disponibles
    if st.button("Genres disponibles"):
        pipeline = [
            {"$project": {"genres": {"$split": ["$genre", ","]}}},
            {"$unwind": "$genres"},
            {"$group": {"_id": "$genres"}},
            {"$sort": {"_id": 1}}
        ]
        result = list(collection.aggregate(pipeline))
        genres = [r["_id"].strip() for r in result]
        st.write("🎭 Genres disponibles :", genres)

    # Q6 - Film avec le plus de revenu
    if st.button("Film avec le plus de revenu"):
        result = collection.find().sort("Revenue (Millions)", -1).limit(1)
        top_film = list(result)[0]
        st.write(f"💰 Film : **{top_film['title']}** - {top_film['Revenue (Millions)']} M$")

    # Q7 - Réalisateurs avec plus de 5 films
    if st.button("Réalisateurs avec plus de 5 films"):
        pipeline = [
            {"$group": {"_id": "$Director", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 5}}},
            {"$sort": {"count": -1}}
        ]
        result = list(collection.aggregate(pipeline))
        for r in result:
            st.markdown(f"- 🎬 **{r['_id']}** : {r['count']} films")

        # Q8 - Genre qui rapporte le plus en moyenne
    if st.button("Genre avec le revenu moyen le plus élevé"):
        pipeline = [
            {"$project": {"genres": {"$split": ["$genre", ","]}, "Revenue": "$Revenue (Millions)"}},
            {"$unwind": "$genres"},
            {"$group": {"_id": "$genres", "avg_revenue": {"$avg": "$Revenue"}}},
            {"$sort": {"avg_revenue": -1}},
            {"$limit": 1}
        ]
        result = list(collection.aggregate(pipeline))
        top_genre = result[0]
        st.write(f"Genre le plus rentable en moyenne : **{top_genre['_id']}** ({round(top_genre['avg_revenue'], 2)} M$)")

    # Q9 - Top 3 films par décennie
    if st.button(" Top 3 films par décennie (rating)"):
        pipeline = [
            {"$addFields": {"decade": {"$multiply": [{"$floor": {"$divide": ["$year", 10]}}, 10]}}},
            {"$sort": {"rating": -1}},
            {"$group": {
                "_id": "$decade",
                "top_films": {"$push": {"title": "$title", "rating": "$rating"}}
            }},
            {"$project": {
                "top_3": {"$slice": ["$top_films", 3]}
            }},
            {"$sort": {"_id": 1}}
        ]
        result = list(collection.aggregate(pipeline))
        for dec in result:
            st.markdown(f"📅 **{dec['_id']}s**")
            for film in dec["top_3"]:
                st.write(f"- {film['title']} ({film['rating']})")

    # Q10 - Film le plus long par genre
    if st.button(" Film le plus long par genre"):
        pipeline = [
            {"$project": {"genres": {"$split": ["$genre", ","]}, "title": 1, "Runtime": "$Runtime (Minutes)"}},
            {"$unwind": "$genres"},
            {"$sort": {"Runtime": -1}},
            {"$group": {"_id": "$genres", "film": {"$first": "$title"}, "runtime": {"$first": "$Runtime"}}}
        ]
        result = list(collection.aggregate(pipeline))
        for r in result:
            st.markdown(f"🎭 **{r['_id']}** : {r['film']} ({r['runtime']} min)")

    # Q11 - Vue des films excellents
    if st.button(" Films avec Metascore > 80 et Revenue > 50M"):
        query = {"Metascore": {"$gt": 80}, "Revenue (Millions)": {"$gt": 50}}
        fields = {"title": 1, "Metascore": 1, "Revenue (Millions)": 1}
        result = list(collection.find(query, fields))
        if result:
            df = pd.DataFrame(result)
            st.dataframe(df)
        else:
            st.warning("Aucun film ne correspond aux critères.")

    # Q12 - Corrélation Runtime vs Revenue
    if st.button("Corrélation entre durée et revenu"):
        data = list(collection.find({"Runtime (Minutes)": {"$ne": None}, "Revenue (Millions)": {"$ne": None}},
                                    {"Runtime (Minutes)": 1, "Revenue (Millions)": 1}))
        df = pd.DataFrame(data)
        if not df.empty:
            runtime = df["Runtime (Minutes)"]
            revenue = df["Revenue (Millions)"]
            correlation = runtime.corr(revenue)
            st.write(f"📈 Corrélation entre durée et revenu : **{round(correlation, 2)}**")

            fig, ax = plt.subplots()
            ax.scatter(runtime, revenue)
            ax.set_xlabel("Durée (min)")
            ax.set_ylabel("Revenu (M$)")
            ax.set_title("Durée des films vs Revenu")
            st.pyplot(fig)
        else:
            st.warning("Pas assez de données pour calculer la corrélation.")

    # Q13 - Évolution de la durée moyenne par décennie
    if st.button("Durée moyenne par décennie"):
        pipeline = [
            {"$addFields": {"decade": {"$multiply": [{"$floor": {"$divide": ["$year", 10]}}, 10]}}},
            {"$group": {"_id": "$decade", "avg_runtime": {"$avg": "$Runtime (Minutes)"}}},
            {"$sort": {"_id": 1}}
        ]
        result = list(collection.aggregate(pipeline))
        if result:
            df = pd.DataFrame(result)
            df.columns = ["Décennie", "Durée moyenne"]
            fig, ax = plt.subplots()
            ax.plot(df["Décennie"], df["Durée moyenne"], marker='o')
            ax.set_title("Évolution de la durée moyenne des films")
            ax.set_xlabel("Décennie")
            ax.set_ylabel("Durée (min)")
            st.pyplot(fig)
        else:
            st.warning("Aucune donnée à afficher.")
        


    st.markdown("---")
    st.subheader("📊 Nombre de films par année (visualisation)")
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    data = list(collection.aggregate(pipeline))

    if data:
        df = pd.DataFrame(data)
        df.columns = ["Année", "Nombre de films"]

        fig, ax = plt.subplots()
        ax.bar(df["Année"], df["Nombre de films"])
        ax.set_xlabel("Année")
        ax.set_ylabel("Nombre de films")
        ax.set_title("Distribution des films par année")

        st.pyplot(fig)
    else:
        st.info("Aucune donnée à afficher.")

    st.markdown("---")
    st.subheader("📊 Nombre de films par genre")

    # Certains genres sont combinés : "Action,Adventure"
    pipeline = [
        {"$project": {
            "genres": {"$split": ["$genre", ","]}
        }},
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]

    genre_data = list(collection.aggregate(pipeline))

    if genre_data:
        genre_df = pd.DataFrame(genre_data)
        genre_df.columns = ["Genre", "Nombre de films"]

        fig2, ax2 = plt.subplots()
        ax2.bar(genre_df["Genre"], genre_df["Nombre de films"])
        ax2.set_xlabel("Genre")
        ax2.set_ylabel("Nombre de films")
        ax2.set_title("Distribution des films par genre")
        plt.xticks(rotation=45, ha='right')

        st.pyplot(fig2)
    else:
        st.info("Aucune donnée de genre à afficher.")    


                  

# Section Neo4j
elif menu == "Neo4j":
    st.header("Accès à Neo4j")
    st.write("Création manuelle du graphe avec les 20 premiers films.")

    if st.button("Créer le graphe"):
        try:
            graph_create_mongo(limit=20)
            st.success("Graphe Neo4j généré avec succès.")
        except Exception as e:
            st.error(f"Erreur lors de la création du graphe : {e}")



st.subheader("Requête Cypher personnalisée")

cypher_query = st.text_area("Écris ta requête Cypher ici :", height=150)

if st.button("Exécuter la requête"):
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as session:
            result = session.run(cypher_query)
            records = result.data()
            if records:
                st.write(records)
            else:
                st.info("La requête a été exécutée, mais aucun résultat à afficher.")
        driver.close()
    except Exception as e:
        st.error(f"Erreur lors de l'exécution de la requête : {e}")

st.markdown("---")
