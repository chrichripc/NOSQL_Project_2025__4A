from neo4j import GraphDatabase
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from app.mongodb_handler import getcollection



def neo4jconnection():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        greeting = session.run("RETURN 'test connexion NEO4j' AS message")
        print(greeting.single()["message"])
    driver.close()


def graph_create_mongo(limit = 20): #test

    # on recupere d'abord les films, pour chaque élément (acteur, genre,titre, etc..) on va soit creer ou merge les noeuds, puis on ajoute la relation en rapport

    client = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    collection = getcollection()
   #print(f"Lecture dans DB : {collection.database.name}, Collection : {collection.name}")
    films = collection.find({"title": {"$exists": True}}).limit(limit)
    #*test_film = collection.find_one()
    #*films = list(films)
    #*print(f"Nombre de films récupérés : {len(films)}")

    with client.session() as session:
        #*print(" Exemple de document :")
        #*print(test_film)

        for film in films:
            title = film.get("title")
            print(f" Traitement du film : {title}")
            if not title:
                continue
            year = film.get("year", None)
            director = film.get("Director", "")
            genres = film.get("genre", "").split(",")
            actors = film.get("Actors", "").split(", ")
# donnée du film

            session.run(
                "MERGE (f:Film {title: $title}) "
                "SET f.year = $year",
                {"title": title, "year": year}
            )

# relations des réalisateurs ------------------------------------------------------
            if director:
                session.run(
                    "MERGE (d:Director {name: $name})",
                    {"name": director}
                )
                session.run(
                    "MATCH (f:Film {title: $title}), (d:Director {name: $name}) "
                    "MERGE (f)-[:DIRECTED_BY]->(d)",
                    {"title": title, "name": director}
                )
#  relations des genres de films ---------------------------------------
            for genre in genres:
                genre = genre.strip()
                if genre:
                    session.run(
                        "MERGE (g:Genre {name: $name})",
                        {"name": genre}
                    )
                    session.run(
                        "MATCH (f:Film {title: $title}), (g:Genre {name: $name}) "
                        "MERGE (f)-[:BELONGS_TO]->(g)",
                        {"title": title, "name": genre}
                    )

# relations des acteurs -----------------------------------------------
            for actor in actors:
                actor = actor.strip()
                if actor:
                    session.run(
                        "MERGE (a:Actor {name: $name})",
                        {"name": actor}
                    )
                    session.run(
                        "MATCH (a:Actor {name: $name}), (f:Film {title: $title}) "
                        "MERGE (a)-[:ACTED_IN]->(f)",
                        {"name": actor, "title": title}
                    )

        print(f"OK, Graphe généré pour {limit} films.")
