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


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
