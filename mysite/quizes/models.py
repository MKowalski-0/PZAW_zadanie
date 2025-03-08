from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # najnowsze quizy na górze


class QuestionType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255, default='Domyślny tekst')
    answer_1 = models.CharField(max_length=255, default='Domyślna odpowiedź 1')  # Dodaj tutaj wartość domyślną
    answer_2 = models.CharField(max_length=255, default='Domyślna odpowiedź 2')
    answer_3 = models.CharField(max_length=255, default='Domyślna odpowiedź 3')
    correct_answer = models.IntegerField()  # 1, 2 lub 3

    def __str__(self):
        return self.question_text



# Wyniki użytkowników
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} - {self.quiz} - {self.score}'
