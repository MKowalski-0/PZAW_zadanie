from django.urls import path
from . import views
from .views import dodaj_quiz, lista_quizow, strona_glowna

urlpatterns = [
    path('', strona_glowna, name='main'),
    path('dodaj-quiz/', dodaj_quiz, name='quiz-add'),
    path('lista-quizow/', lista_quizow, name='quiz-list'),
]