from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('main/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('main/<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('quizzes/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
]