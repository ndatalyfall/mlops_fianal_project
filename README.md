# M1 DSIA - Projet MLOps : API FastAPI conteneurisée & Docker Hub

Ce projet consiste à concevoir, conteneuriser avec Docker et publier une API REST complète développée avec **FastAPI**. L'API permet la consultation et la gestion (CRUD complet) d'un catalogue d'outils MLOps stockés dans un fichier `data.json`.

---

## 📌 Présentation du Projet & Thème

- **Thème choisi** : Catalogue d'Outils et Modèles MLOps (Experiment Tracking, Data Versioning, Model Monitoring, Model Serving, Feature Store, etc.).
- **Projet** : M1 DSIA - Année universitaire 2024–2025
- **Membres de l'équipe** : [Insérer les noms / prénoms des membres du groupe]
- **Image Docker Hub** : [https://hub.docker.com/r/<username>/dsia-api](https://hub.docker.com/r/<username>/dsia-api)

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

## 📝 Exemples de Requêtes & Réponses JSON

### 1. `POST /items` (Ajouter un élément)
**Body de la requête** :
```json
{
  "nom": "KubeFlow",
  "categorie": "Orchestration",
  "prix": 0.0,
  "description": "Plateforme MLOps dédiée au déploiement de workflows sur Kubernetes.",
  "statut": "Production"
}
```
**Réponse `201 Created`** :
```json
{
  "id": 11,
  "nom": "KubeFlow",
  "categorie": "Orchestration",
  "prix": 0.0,
  "description": "Plateforme MLOps dédiée au déploiement de workflows sur Kubernetes.",
  "statut": "Production"
}
```

### 2. `PUT /items/11` (Remplacement complet)
**Body de la requête** :
```json
{
  "nom": "KubeFlow Pipelines",
  "categorie": "Orchestration & Pipelines",
  "prix": 0.0,
  "description": "Système de pipelines pour Kubeflow.",
  "statut": "Production"
}
```

### 3. `PATCH /items/11` (Modification partielle)
**Body de la requête** :
```json
{
  "prix": 10.0,
  "statut": "Beta"
}
```

### 4. `DELETE /items/11` (Suppression)
**Réponse `200 OK`** :
```json
{
  "message": "Élément id=11 supprimé avec succès.",
  "deleted_item": { ... }
}
```

---

## 🛠️ Exécution en Local

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

## 🚀 Conteneurisation & Publication Docker Hub

### Build de l'image Docker
```bash
docker build -t dsia-api:v1.0 .
```

### Lancement du conteneur
```bash
docker run -d -p 8000:8000 --name mlops-api-container dsia-api:v1.0
```

### Push sur Docker Hub
```bash
docker login
docker tag dsia-api:v1.0 <username>/dsia-api:v1.0
docker push <username>/dsia-api:v1.0
```
