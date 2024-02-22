from pymongo import MongoClient
import os
import json

def get_dev_secrets():
    dev_secrets = json.loads(os.environ.get('DEV_SECRETS'))
    return {
        'username': dev_secrets["MONGO_DB_USERNAME"],
        'password': dev_secrets["MONGO_DB_PASSWORD"],
        'uri': dev_secrets["MONGO_DB_URI"]
    }

def create_mongo_client(db_name):
    secrets = get_dev_secrets()
    uri = f"mongodb+srv://{secrets['username']}:{secrets['password']}@{secrets['uri']}/{db_name}?retryWrites=true&w=majority"
    return MongoClient(uri)

def get_apollo_db():
    pass

def get_astra_db():
    pass

def get_chrona_db():
    pass

def get_anthropos_db():
    client = create_mongo_client("anthropos")
    return client["anthropos"]
