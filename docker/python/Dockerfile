FROM python:3.12-slim

# Actualiza e instala paquetes necesarios
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean

# Instala herramientas adicionales de Python
RUN pip install --no-cache-dir pipenv
#RUN pip install Flask