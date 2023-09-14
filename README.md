# Blog Backend

Este es el backend de un blog interactivo desarrollado utilizando Django.

## Descripción

El backend proporciona la lógica y el manejo de datos para el blog interactivo. Utiliza Django para gestionar las bases de datos y servir los datos al front-end de la aplicación.

## Requisitos de Instalación

- Python
- Django

## Instalación

1. Clona el repositorio: `git clone https://github.com/Mahuel18/blogback.git`
2. Navega al directorio del proyecto: `cd blog-backend`
3. Instala las dependencias: `pip install -r requirements.txt`
4. Realiza las migraciones: `python manage.py migrate`

## Cómo Usar

1. Inicia el servidor: `python manage.py runserver`
2. El backend estará disponible en `http://localhost:8000`

## Ejemplos de Código

```python
# Ejemplo de código Django (models.py)
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
