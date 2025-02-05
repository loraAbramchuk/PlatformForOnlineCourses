from .models import Course, Lesson
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
    return render(request, 'lesson_detail.html', {'lesson': lesson})