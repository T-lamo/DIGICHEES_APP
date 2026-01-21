# 🚀 API FastAPI – Projet Backend

Ce projet est une **API backend développée avec FastAPI**, utilisant **SQLModel** pour l’accès aux données et **MariaDB** comme base de données.  
L’application peut être lancée **en local avec un environnement virtuel Python** ou **via Docker Compose**.


## Test With
| Username | Password  |
|----------|-----------|
| admin    | admin123  |
| colis    | colis123  |
| stock    | stock123  |

---

## 🧱 Stack technique

- **Python 3.12**
- **FastAPI**
- **SQLModel**
- **MariaDB**
- **PyMySQL**
- **python-dotenv**
- **Docker & Docker Compose**

---

## 📁 Structure du projet

```
mon-projet-api/
├── src/
│   ├── main.py
|   ├── models/   
|   ├── repositories/ 
|   ├── routes/ 
|   ├── services/ 
|   ├── utils/ 
│   ├── conf/
│   │   └── db/
│   │       ├── database.py
│   │       └── settings.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── .env.docker
├── requirements.txt
└── README.md
```

---

## 🔐 Variables d’environnement

Les informations sensibles sont stockées dans le fichier `.env.docker` (non versionné).

### Exemple de `.env.docker`

```
DB_HOST={db}
DB_PORT={3306}
DB_USER={root}
DB_PASSWORD={password}
DB_NAME={apidb}

MYSQL_ROOT_PASSWORD={securepassword}
MYSQL_DATABASE={apidb}
MYSQL_USER={admin}
MYSQL_PASSWORD={Admin123!}

PORT_DB_VISUALISATION={3307}
```

---

## 🧪 Installation locale (sans Docker)


### Créer l’environnement virtuel

```
python -m venv .venv
```

### Activer l’environnement

```
source apivenv/bin/activate
```

### Installer les dépendances

```
pip install pymysql python-dotenv fastapi sqlmodel
pip freeze > requirements.txt
pip install -r requirements.txt
```

### Lancer l’API

```
uvicorn src.main:app --reload
 ENV=dev uvicorn src.main:app --reload
 ENV_FILE=.env.test pytest
```

Accès :
- API : http://127.0.0.1:8000
- Swagger : http://127.0.0.1:8000/docs

---

## 🐳 Lancement avec Docker

### Prérequis
- Docker
- Docker Compose v2+

### Démarrage

```
docker compose --env-file .env.docker up --build
```

### Accès aux services

| Service | URL |
|------|----|
| FastAPI | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Adminer | http://localhost |
| MariaDB | localhost:3307 |

---

## 🛠️ Développement

- Live reload activé
- Volumes montés pour `src/` et `tests/`
- Rechargement automatique du code

---

## 📌 Commandes utiles

```
docker compose down
docker compose down -v
docker compose --env-file .env.docker config
docker compose exec fastapi env | grep DB
```

---

## 👨‍💻 Auteur

Projet développé avec **FastAPI**, **Docker** et **MariaDB** dans un contexte pédagogique.




## Usefull script
 -  find . -type d -name "__pycache__" -exec rm -rf {} +
 -  find . -type f -name "*.pyc" -delete


 ## openssl rand -hex 32
 