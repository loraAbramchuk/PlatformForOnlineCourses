from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'quizzes', views.QuizViewSet)
router.register(r'certificates', views.CertificateViewSet)


urlpatterns = [
    # Web URLs
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('course/<int:course_id>/complete/', views.complete_course, name='complete_course'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('my_certificates/', views.my_certificates, name='my_certificates'),
    
    # API URLs
    path('api/', include(router.urls)),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),


]