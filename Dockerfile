# Usa una imagen base de Python
FROM python:3.9

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto 5000
EXPOSE 5000

# Define el comando de inicio
CMD ["python3", "wsgi.py"]
