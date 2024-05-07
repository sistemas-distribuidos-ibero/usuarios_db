# Utiliza una imagen oficial de Python como base
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala las dependencias del proyecto
# Copia primero solo los archivos necesarios para la instalación de dependencias para aprovechar la caché de Docker layers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos de la aplicación necesarios al directorio de trabajo del contenedor
# Asegurándonos de que .dockerignore excluya archivos innecesarios para reducir el tamaño de la imagen
COPY . .

# Configura la variable de entorno para encontrar la aplicación Flask
ENV FLASK_APP=app/app.py

# Expone el puerto 5000 para que sea accesible fuera del contenedor
EXPOSE 5000

# Define el comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
