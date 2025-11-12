# ---- Image de base ----
FROM python:3.11-slim

# ---- Dossier de travail ----
WORKDIR /app

# ---- Copier les fichiers du projet ----
COPY . .

# ---- Installer les dépendances ----
RUN pip install --upgrade pip
RUN pip install django djongo pymongo

# ---- Lancer le serveur ----
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
