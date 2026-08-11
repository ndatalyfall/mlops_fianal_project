# Image de base légère Python 3.11
FROM python:3.11-slim

# Empêche Python d'écrire des fichiers .pyc et force l'affichage immédiat des logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie et installation des dépendances en utilisant le cache des layers Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source de l'application (contient app/main.py et app/data.json)
COPY app/ ./app/

# Exposition du port 8000 pour FastAPI / Uvicorn
EXPOSE 8000

# Commande de démarrage du serveur Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
