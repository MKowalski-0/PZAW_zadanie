from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Strona główna
    path('register/', views.register, name='register'),  # Rejestracja
    path('create_quiz/', views.create_quiz, name='create_quiz'),  # Tworzenie quizu
    path('quiz/<int:quiz_id>/', views.solve_quiz, name='solve_quiz'),  # Rozwiązywanie quizu
    path('result/<int:result_id>/', views.quiz_result, name='quiz_result'),  # Wyniki quizu
    path('add_questions/<int:quiz_id>/', views.add_questions, name='add_questions'),  # Dodawanie pytań
]
