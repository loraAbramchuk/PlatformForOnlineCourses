from django.contrib import admin

# Register your models here.

from .models import Course, Lesson, Quiz, Certificate

class LessonInLine(admin.TabularInline):
    model = Lesson
    extra = 1

class QuizInLine(admin.TabularInline):
    model = Quiz
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'start_date', 'price', 'currency']
    search_fields = ['title', 'description']
    list_filter = ['start_date', 'price']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    search_fields = ['title']
    list_filter = ['course']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['question', 'lesson']
    search_fields = ['question']
    list_filter = ['lesson']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'date_issued']
    search_fields = ['user__username', 'course__title']
    list_filter = ['date_issued']

admin.site.site_header = "Панель администратора OnlineCourses"
admin.site.site_title = "OnlineCourses Admin"  
admin.site.index_title = "Добро пожаловать в админку OnlineCourses!"