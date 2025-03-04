from django.db import models
from django.contrib.auth.models import User

# Typy pytań
class QuestionType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Pytania w quizie
class Question(models.Model):
    TEXT = 'text'
    CHOICE = 'choice'
    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (CHOICE, 'Choice'),
    ]
    text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=TEXT)
    correct_answer = models.CharField(max_length=200)
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

# Quiz
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField(Question)
    # Dodatkowe pola, takie jak wynik, mogą być przechowywane w innym modelu

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # najnowsze quizy na górze

# Wyniki użytkowników
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} - {self.quiz} - {self.score}'
