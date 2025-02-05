from .forms import QuizForm
from .models import Course, Lesson, Quiz
from django.shortcuts import get_object_or_404, redirect, render

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
