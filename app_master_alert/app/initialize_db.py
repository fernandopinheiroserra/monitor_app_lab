import os
from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
DATABASE_NAME = os.getenv("DATABASE_NAME", "master_alert")
COLLECTIONS = ["pings", "absences"]

def get_mongo_client():
    mongo_url = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
    return MongoClient(mongo_url)

def initialize_database():
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    
    for collection_name in COLLECTIONS:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' criada.")
        else:
            print(f"Collection '{collection_name}' já existe.")
            
    print(f"Banco de dados '{DATABASE_NAME}' inicializado com sucesso.")
    return db
