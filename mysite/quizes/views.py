from django.shortcuts import render, redirect
from .models import Quiz, Pytanie
from django.forms import ModelForm

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

def strona_glowna(request):
    return render(request, 'quizes/main.html')

def dodaj_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz-list')
    else:
        form = QuizForm()
    return render(request, 'quizes/dodaj_quiz.html', {'form': form})

def lista_quizow(request):
    quizes = Quiz.objects.all()
    return render(request, 'quizes/lista_quizow.html', {'quizes': quizes})
