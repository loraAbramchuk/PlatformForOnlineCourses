from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .forms import QuizForm
from .models import Course, Lesson, Quiz, Certificate
from .serializers import CourseSerializer, LessonSerializer, QuizSerializer, CertificateSerializer

def index(request):
    """Главная страница"""
    return render(request, 'index.html')

@login_required
def dashboard(request):
    courses = Course.objects.all()
    return render(request, 'dashboard.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    return render(request, 'course_detail.html', {'course': course, 'lessons': lessons})

@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.students.add(request.user)
    messages.success(request, f"Вы успешно записались на курс '{course.title}'!")
    return redirect('course_detail', course_id=course.id)

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
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

@login_required
def complete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    request.user.completed_courses.add(course)
    Certificate.objects.create(user=request.user, course=course)
    messages.success(request, f"Сертификат за курс '{course.title}' успешно создан! 🎓")
    return redirect('dashboard')

@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(user=request.user)
    return render(request, 'my_certificates.html', {'certificates': certificates})

# API ViewSets
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'status': 'enrolled'})

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        quiz = self.get_object()
        answer = request.data.get('answer')
        is_correct = answer == quiz.correct_answer
        return Response({
            'is_correct': is_correct,
            'message': "Правильно!" if is_correct else "Неправильно!"
        })

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user)