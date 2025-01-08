from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł Quizu")
    description = models.TextField(blank=True, verbose_name="Opis Quizu")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Pytanie(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='pytania')
    question_text = models.CharField(max_length=300, verbose_name="Question Text")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text
