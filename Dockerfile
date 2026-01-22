# 1️⃣ Image Python officielle
FROM python:3.12-slim

# 2️⃣ Dossier de travail dans le container
WORKDIR /app

# 3️⃣ Copier les dépendances
COPY requirements.txt .
COPY .env.docker .env.docker


# 4️⃣ Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copier le code source
COPY src ./src

# 6️⃣ Exposer le port FastAPI
EXPOSE 8000

# 7️⃣ Lancer l'application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "src"]
