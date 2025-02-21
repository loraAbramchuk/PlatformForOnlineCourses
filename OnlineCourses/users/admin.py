from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages

from .models import CustomUser
from main.models import Course

from django.templatetags.static import static

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'display_completed_courses')
    actions = ['mark_all_courses_completed', 'unmark_all_courses_completed']

    def mark_all_courses_completed(self, request, queryset):
        all_courses = Course.objects.all()
        for user in queryset:
            user.completed_courses.set(all_courses)  # ✅ Добавляем все курсы в список завершённых
        self.message_user(request, f"{queryset.count()} студентов завершили все курсы.", messages.SUCCESS)

    mark_all_courses_completed.short_description = "✅ Отметить прохождение всех курсов"

    def unmark_all_courses_completed(self, request, queryset):
        for user in queryset:
            user.completed_courses.clear()  # ✅ Очищаем список завершённых курсов
        self.message_user(request, f"{queryset.count()} студентов теперь не имеют завершённых курсов.", messages.WARNING)

    unmark_all_courses_completed.short_description = "❌ Отменить прохождение всех курсов"


    def display_completed_courses(self, obj):
        return ", ".join([course.title for course in obj.completed_courses.all()]) or "Нет"

    display_completed_courses.short_description = "Завершённые курсы"

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['custom_styles'] = static('admin/custom.css')  # Добавляем путь к стилям
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(CustomUser, CustomUserAdmin)