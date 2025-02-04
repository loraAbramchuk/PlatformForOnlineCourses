from .models import Course
from django.shortcuts import get_object_or_404, redirect, render

def dashboard(request):
    courses = Course.objects.all()
    return render(request, 'dashboard.html', {'courses' : courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.is_authenticated:
        course.students.add(request.user)
    return redirect('course_detail', course_id=course.id)