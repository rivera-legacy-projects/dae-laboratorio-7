from django.db import models


# Modelo que representa un cuestionario (Quiz)
class Quiz(models.Model):
    # Título del cuestionario, máximo 200 caracteres
    title = models.CharField(max_length=200)
    # Descripción del cuestionario
    description = models.TextField()
    # Fecha y hora de creación, se asigna automáticamente al crear el objeto
    created_at = models.DateTimeField(auto_now_add=True)

    # Representación en texto del objeto Quiz
    def __str__(self):
        return self.title
