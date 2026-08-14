# Membres du projet
- Seynabou Gueye
- Mamadou Demba Fall
- Ndataly Fall

# M1 DSIA - Projet MLOps : API FastAPI conteneurisée, Docker Hub & Pipeline CI/CD

Ce projet consiste à concevoir, conteneuriser avec Docker, automatiser via un pipeline CI/CD GitHub Actions et publier une API REST complète développée avec **FastAPI**. L'API permet la consultation et la gestion (CRUD complet) d'un catalogue d'outils MLOps stockés dans un fichier `data.json`.

---

## 📌 Présentation du Projet & Thème

- **Thème choisi** : Catalogue d'Outils et Modèles MLOps (Suivi d'expériences, Contrôle de version des données, Surveillance de modèles, Déploiement de modèles, Magasin de caractéristiques, etc.).
- **Projet** : M1 DSIA - Année universitaire 2024–2025
- **Nom de l'image Docker** : `mlops_api`
- **Membres de l'équipe** : [Insérer les noms / prénoms des membres du groupe]
- **Image Docker Hub publique** : [https://hub.docker.com/r/ndataly/mlops_api](https://hub.docker.com/r/ndataly/mlops_api)

---

## 🔄 Pipeline CI/CD (GitHub Actions)

Un workflow d'intégration et de déploiement continu est configuré dans [.github/workflows/ci-cd.yml](file:///.github/workflows/ci-cd.yml) :

1. **Intégration Continue (CI)** :
   - Déclenchée à chaque `push` ou `pull request` sur les branches `main` / `master`.
   - Installation de Python 3.11 et des dépendances (`requirements.txt`).
   - Exécution de la suite de tests automatisés (`pytest tests/test_api.py`).

2. **Déploiement Continu (CD)** :
   - Exécutée uniquement si les tests CI réussissent lors d'un `push` sur la branche principale.
   - Connexion automatique à Docker Hub via les secrets GitHub.
   - Build et publication automatique de l'image `ndataly/mlops_api:latest` et `ndataly/mlops_api:v1.0` sur Docker Hub.

### 🔑 Secrets à configurer sur GitHub
Dans votre dépôt GitHub, allez dans **Settings > Secrets and variables > Actions** et ajoutez :
- `DOCKER_HUB_USERNAME` : `ndataly`
- `DOCKER_HUB_TOKEN` : Un token d'accès généré sur Docker Hub (dans *Account Settings > Personal Access Tokens*).

---

## 🛣️ Tableau des Endpoints de l'API

| Méthode | Route | Description | Code HTTP |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Message d'accueil et version de l'API | `200 OK` |
| `GET` | `/health` | Statut de l'API | `200 OK` |
| `GET` | `/items` | Obtenir tous les éléments | `200 OK` |
| `GET` | `/items/{id}` | Obtenir un élément par son ID | `200 OK` / `404 Not Found` |
| `POST` | `/items` | Ajouter un nouvel élément | `201 Created` |
| `PUT` | `/items/{id}` | Remplacement complet d'un élément par son ID | `200 OK` / `404 Not Found` |
| `PATCH` | `/items/{id}` | Modification partielle d'un élément par son ID | `200 OK` / `404 Not Found` |
| `DELETE` | `/items/{id}` | Supprimer un élément par son ID | `200 OK` / `404 Not Found` |

---

## 🛠️ Exécution en Local (sans Docker)

### Lancement du serveur avec Uvicorn
```bash
uvicorn app.main:app --reload
```
L'API est accessible sur `http://127.0.0.1:8000`.  
Documentation Swagger interactive : **`http://127.0.0.1:8000/docs`**.

### Lancer la suite de tests (pytest)
```bash
pytest tests/test_api.py -v
```

---

## 🚀 Conteneurisation & Test Docker Local

### 1. Build de l'image Docker
```bash
docker build -t ndataly/mlops_api:v1.0 .
```

### 2. Lancement du conteneur
```bash
docker run -d -p 8000:8000 --name mlops-api-container ndataly/mlops_api:v1.0
```
Tester l'API conteneurisée sur `http://localhost:8000/health`.

### 3. Arrêt du conteneur
```bash
docker stop mlops-api-container
docker rm mlops-api-container
```

---

## 📦 Publication Manuelle sur Docker Hub

```bash
docker login
docker tag mlops_api:v1.0 ndataly/mlops_api:v1.0
docker push ndataly/mlops_api:v1.0
```
