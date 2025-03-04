# quizes/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count
from django.contrib import messages
from .models import Quiz, Question, QuizResult
from .forms import QuizForm, QuestionForm

# Strona główna
def home(request):
    newest_quizzes = Quiz.objects.all()[:10]  # 10 najnowszych quizów
    popular_quizzes = Quiz.objects.annotate(num_results=Count('quizresult')).order_by('-num_results')[:10]  # 10 najpopularniejszych quizów
    return render(request, 'quizes/home.html', {'newest_quizzes': newest_quizzes, 'popular_quizzes': popular_quizzes})

# Rejestracja użytkownika
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.save())
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'quizes/register.html', {'form': form})

# Logowanie użytkownika
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Zalogowano jako {username}!')
                return redirect('home')  # Przekierowanie na stronę główną po zalogowaniu
            else:
                messages.error(request, 'Niepoprawny login lub hasło.')
        else:
            messages.error(request, 'Błąd logowania.')
    else:
        form = AuthenticationForm()
    return render(request, 'quizes/login.html', {'form': form})

# Wylogowywanie użytkownika
def logout_view(request):
    logout(request)
    return redirect('home')  # Przekierowanie na stronę główną po wylogowaniu

# Formularz tworzenia quizu
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quizes/create_quiz.html', {'form': form})

# Dodawanie pytań do quizu
def add_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        for i in range(int(request.POST.get('num_questions'))):
            question_form = QuestionForm(request.POST, prefix=f'question_{i}')
            if question_form.is_valid():
                question = question_form.save()
                quiz.questions.add(question)
        return redirect('home')
    else:
        num_questions = 1
    return render(request, 'quizes/add_questions.html', {'quiz': quiz, 'num_questions': num_questions})

# Rozwiązywanie quizu
def solve_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.POST.get(str(question.id))
            if user_answer == question.correct_answer:
                score += 1
        QuizResult.objects.create(user=request.user, quiz=quiz, score=score)
        return redirect('quiz_result', result_id=score)
    return render(request, 'quizes/solve_quiz.html', {'quiz': quiz, 'questions': questions})

# Wyniki quizu
def quiz_result(request, result_id):
    result = QuizResult.objects.get(id=result_id)
    return render(request, 'quizes/quiz_result.html', {'result': result})
