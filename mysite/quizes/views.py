from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count
from django.contrib import messages
from .models import Quiz, Question, QuizResult
from .forms import QuizForm, QuestionForm

# Strona główna
def home(request):
    newest_quizzes = Quiz.objects.all()[:10]  
    popular_quizzes = Quiz.objects.annotate(num_results=Count('quizresult')).order_by('-num_results')[:10]
    return render(request, 'quizes/home.html', {'newest_quizzes': newest_quizzes, 'popular_quizzes': popular_quizzes})

# Rejestracja użytkownika
def register(request):
    if request.user.is_authenticated:
        return redirect('home')  # Jeśli użytkownik jest już zalogowany, przekieruj na stronę główną

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Rejestracja zakończona sukcesem!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'quizes/register.html', {'form': form, 'home_link': True})

# Logowanie użytkownika
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Jeśli użytkownik jest już zalogowany, przekieruj na stronę główną

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Zalogowano jako {username}!')
                return redirect('home')  
            else:
                messages.error(request, 'Niepoprawny login lub hasło.')
        else:
            messages.error(request, 'Błąd logowania.')
    else:
        form = AuthenticationForm()
    return render(request, 'quizes/login.html', {'form': form, 'home_link': True})

# Wylogowywanie użytkownika
def logout_view(request):
    logout(request)
    messages.info(request, 'Zostałeś wylogowany.')
    return redirect('home')

# Tworzenie quizu (tylko dla zalogowanych użytkowników)
@login_required
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
    return render(request, 'quizes/create_quiz.html', {'form': form, 'home_link': True})

@login_required
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        num_questions = int(request.POST.get('num_questions', 1))  # Liczba pytań
        questions_added = 0

        # Dodawanie pytań
        for i in range(num_questions):
            question_form = QuestionForm(request.POST, prefix=f'question_{i}')
            if question_form.is_valid():
                question = question_form.save()
                quiz.questions.add(question)
                questions_added += 1

        if questions_added > 0:
            messages.success(request, f'Dodano {questions_added} pytania do quizu!')
        else:
            messages.error(request, 'Nie udało się dodać żadnego pytania.')

        return render(request, 'quizes/add_questions.html', {
            'quiz': quiz,
            'num_questions': num_questions,
            'questions_added': questions_added,
            'home_link': True
        })
    
    # Jeśli nie ma POST, ustawiamy domyślną liczbę pytań
    else:
        num_questions = 1  # Domyślnie jedna odpowiedź
    
    return render(request, 'quizes/add_questions.html', {
        'quiz': quiz,
        'num_questions': num_questions,
        'home_link': True
    })

@login_required
def solve_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Pobieramy pytania związane z quizem

    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.POST.get(str(question.id))  # Pobieramy odpowiedź użytkownika
            if user_answer == question.correct_answer:
                score += 1

        result = QuizResult.objects.create(user=request.user, quiz=quiz, score=score)
        return redirect('quiz_result', result_id=result.id)

    return render(request, 'quizes/solve_quiz.html', {'quiz': quiz, 'questions': questions, 'home_link': True})

# Wyniki quizu
@login_required
def quiz_result(request, result_id):
    result = get_object_or_404(QuizResult, id=result_id)
    return render(request, 'quizes/quiz_result.html', {'result': result, 'home_link': True})
