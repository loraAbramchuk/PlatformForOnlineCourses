from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import QuizForm
from .models import Course, Lesson, Quiz, Certificate
from django.shortcuts import get_object_or_404, redirect, render

@login_required
def dashboard(request):
    courses = Course.objects.all()
    return render(request, 'dashboard.html', {'courses' : courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # lessons = get_object_or_404(Lesson, id=course.id)
    lessons = course.lessons.all()
    return render(request, 'course_detail.html', {'course': course, 'lessons': lessons})

def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.is_authenticated:
        course.students.add(request.user)
    return redirect('course_detail', course_id=course.id)

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    # quizes = lesson.quizzes.all()
    return render(request, 'lesson_detail.html', {'lesson': lesson})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    result = None

    if request.method == 'POST':
        form = QuizForm(request.POST, quiz=quiz)
        if form.is_valid():
            user_answer = form.cleaned_data['answer']
            result = "✅ Правильно!" if user_answer == quiz.correct_answer else "❌ Неправильно!"

    else:
        form = QuizForm(quiz=quiz)

    return render(request, 'quizes_detail.html', {'quiz': quiz, 'form': form, 'result': result})

def complete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.is_authenticated:
        Certificate.objects.create(user=request.user, course=course)  # Создаём сертификат
        messages.success(request, f"Сертификат за курс '{course.title}' успешно создан! 🎓")  # ✅ Теперь messages работает

    return redirect('dashboard')  # Возвращаем пользователя на главную


def my_certificates(request):
    certificates = Certificate.objects.filter(user=request.user)
    return render(request, 'my_certificates.html', {'certificates': certificates})