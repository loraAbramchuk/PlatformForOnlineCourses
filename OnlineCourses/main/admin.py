import openpyxl

from django.contrib import admin
from django.http import HttpResponse
from django.core.mail import EmailMessage
import io

import pandas as pd
from datetime import datetime
from django.utils import timezone

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
    actions = ['export_data_to_excel']

    def export_data_to_excel(self, request, queryset):
        # Создаем Excel файл в памяти
        output = io.BytesIO()

        # Функция для преобразования datetime с timezone в datetime без timezone
        def convert_timezone_aware_dates(df):
            for column in df.select_dtypes(include=['datetime64[ns, UTC]']).columns:
                df[column] = df[column].dt.tz_localize(None)
            return df

        # Создаем словарь с данными для каждой модели
        data = {
            'Courses': convert_timezone_aware_dates(pd.DataFrame(list(Course.objects.all().values()))),
            'Lessons': convert_timezone_aware_dates(pd.DataFrame(list(Lesson.objects.all().values()))),
            'Quizzes': convert_timezone_aware_dates(pd.DataFrame(list(Quiz.objects.all().values()))),
            'Certificates': convert_timezone_aware_dates(pd.DataFrame(list(Certificate.objects.all().values())))
        }

        # Записываем каждую таблицу на отдельный лист
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name, df in data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Подготавливаем email
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'database_export_{timestamp}.xlsx'

        email = EmailMessage(
            'Экспорт базы данных',
            'Во вложении находится файл с экспортом данных из базы.',
            'larachka.06@gmail.com',
            ['larachka.06@gmail.com']
        )

        # Прикрепляем файл
        email.attach(filename, output.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # Отправляем email
        email.send()

        self.message_user(request, 'Данные успешно экспортированы и отправлены на email')

    export_data_to_excel.short_description = "Экспортировать данные в Excel и отправить на email"

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