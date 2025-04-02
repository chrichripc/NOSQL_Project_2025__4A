from app.mongodb_handler import getcollection, import_movies_from_file
from app.neo4j_handler import neo4jconnection
from app.neo4j_handler import graph_create_mongo
from app.mongodb_handler import clear_test_documents


def test_insert():
    #collection = getcollection()
    #result = collection.insert_one({"test": "connexion réussie"})
    #print("ID du document inséré :", result.inserted_id)
    pass
if __name__ == "__main__":
    clear_test_documents()
    import_movies_from_file("data/movies.json")
    neo4jconnection()
    graph_create_mongo(limit=20)


#test