# Imagen base de Python slim para tener menos peso
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Paquetes del sistema que a veces ayudan a compilar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la app
COPY app ./app

# Exponer el puerto del servidor uvicorn
EXPOSE 8000

# Comando de arranque: levantar FastAPI con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
