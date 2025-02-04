from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('main/<int:course_id>/', views.course_detail, name='course_detail'),
    path('main/<int:course_id>/enroll/', views.enroll, name='enroll'),
]