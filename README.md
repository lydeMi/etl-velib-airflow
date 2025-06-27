# 🚲 Projet ETL Vélib – Données temps réel avec Airflow, Docker & MongoDB

Bienvenue dans ce projet ! Ici, on a mis en place un pipeline complet qui récupère automatiquement les données de disponibilité des stations Vélib (depuis Open Data Paris), les traite légèrement, puis les stocke proprement dans une base de données MongoDB.  
Tout ça tourne tranquillement grâce à **Airflow**, dans un environnement **Dockerisé**, et avec une configuration sécurisée via `.env`.

---

## 🤖 Ce que fait le projet (en clair)

- 🔍 Il va chercher les données des stations Vélib toutes les 30 minutes
- 📦 Il ajoute un horodatage à chaque enregistrement
- 🧠 Il les stocke dans **MongoDB** (en local, pas besoin d’Atlas !)
- 🧩 Le tout est automatisé et orchestré par **Airflow**
- 🔐 Et on garde les infos sensibles dans un fichier `.env.local` (jamais versionné)

---

## 🧰 Les outils utilisés

| Technologie | Rôle |
|-------------|------|
| **Python** | Scripts d’ingestion et transformation |
| **Docker / Compose** | Conteneurisation et orchestration locale |
| **MongoDB** | Stockage des données |
| **Airflow** | Orchestration ETL (planification, exécution) |
| **Open Data Paris** | Source des données Vélib |

---

## 🚀 Lancer le projet en 3 étapes

### 1. Cloner le dépôt

```bash
git clone https://github.com/lydeMi/etl-velib-airflow.git
cd etl_velib_project/airflow

