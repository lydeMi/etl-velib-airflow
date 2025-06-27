import os
import logging
from typing import List, Dict
import requests
from pymongo import MongoClient, errors
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# 🔐 Chargement automatique de .env.local si présent, sinon .env
env_dir = Path(__file__).resolve().parent.parent / "env_files"
env_local = env_dir / ".env.local"
env_file = env_local if env_local.exists() else env_dir / ".env"
load_dotenv(dotenv_path=env_file)

# 📋 Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", force=True)

def fetch_belib_data(limit: int = 50) -> List[Dict]:
    """
    Récupère les données de l'API Vélib via Open Data Paris.
    """
    api_url = os.getenv("API_URL")
    if not api_url:
        raise EnvironmentError("La variable API_URL n'est pas définie dans le fichier .env")

    try:
        logging.info(f"Appel de l'API Vélib avec une limite de {limit} enregistrements...")
        response = requests.get(api_url)
        response.raise_for_status()

        json_data = response.json()
        records = json_data.get("records", [])
        logging.info(f"{len(records)} enregistrements récupérés avec succès.")
        return [record.get("fields", {}) for record in records]

    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur HTTP lors de l'appel à l'API : {e}")
        raise

def insert_to_mongodb(data: List[Dict]) -> None:
    """
    Insère les données récupérées dans MongoDB, avec un timestamp d'insertion.
    """
    mongo_uri = os.getenv("MONGO_URI")
    dbname = os.getenv("MONGO_DBNAME")
    collection_name = os.getenv("MONGO_COLLECTION", "belib")

    if not all([mongo_uri, dbname]):
        raise EnvironmentError("Les variables MONGO_URI ou MONGO_DBNAME sont manquantes.")

    try:
        client = MongoClient(mongo_uri)
        db = client[dbname]
        collection = db[collection_name]

        if data:
            # 🕒 Ajout du champ insertion_timestamp
            now = datetime.utcnow().isoformat()
            for doc in data:
                doc["insertion_timestamp"] = now

            result = collection.insert_many(data)
            logging.info(f"{len(result.inserted_ids)} documents insérés dans la collection '{collection_name}'.")
        else:
            logging.warning("Aucune donnée à insérer.")

    except errors.PyMongoError as e:
        logging.error(f"Erreur MongoDB : {e}")
        raise

    finally:
        client.close()
        logging.info("Connexion MongoDB fermée.")

def run_belib_pipeline():
    """
    Pipeline complet à exécuter depuis Airflow ou en local.
    """
    try:
        data = fetch_belib_data(limit=50)
        insert_to_mongodb(data)
        logging.info("Pipeline ETL exécuté avec succès.")
        print("✅ Pipeline terminé")
    except Exception as e:
        logging.error(f"Échec du pipeline ETL : {e}")
        print("❌ Pipeline échoué")

# ✅ Permet l'exécution directe
if __name__ == "__main__":
    run_belib_pipeline()
