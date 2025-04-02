from pymongo import MongoClient
from app.config import MONGO_URI
from app.config import MONGO_DB_NAME, MONGO_COLLECTION

import json
from pymongo import MongoClient
from app.config import MONGO_URI



MONGO_DB_NAME = "entertainment"
MONGO_COLLECTION = "films"


def getcollection():


    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    return db[MONGO_COLLECTION]

def import_movies_from_file(filepath):
    client = MongoClient(MONGO_URI)
    db = client["entertainment"]
    collection = db["films"]
    collection = db["films"]
    #print(f"Importation dans DB : {db.name}, Collection : {collection.name}")

    with open(filepath, 'r') as f:
        docs = [] #probleme avec id100 insertion du document
        for line in f:
            doc = json.loads(line)
            doc.pop("_id", None) 
            docs.append(doc)

    result = collection.insert_many(docs)
    print(f"OK {len(result.inserted_ids)} films insérés dans la collection.")

def clear_test_documents():
    collection = getcollection()
    result = collection.delete_many({"test": {"$exists": True}})
    #print(f" {result.deleted_count} documents de test supprimés.")
