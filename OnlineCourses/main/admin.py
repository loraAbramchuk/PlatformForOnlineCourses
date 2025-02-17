from django.contrib import admin

# Register your models here.

from .models import Course, Lesson, Quiz

class LessonInLine(admin.TabularInline):
    model = Lesson
    extra = 1

class QuizInLine(admin.TabularInline):
    model = Quiz
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','content', 'start_date', 'get_students', 'admin_display_price_with_currency')
    list_filter = ('title', 'start_date')
    search_fields = ('title',)
    inlines = [LessonInLine]

    def get_students(self, obj):
        return ", ".join([student.username for student in obj.students.all()])  # ✅ Показываем список имён

    get_students.short_description = "Студенты"


    def admin_display_price_with_currency(self, obj):
        return f"{obj.price} {obj.currency}"

    admin_display_price_with_currency.short_description = "Цена (с валютой)"


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuizInLine]

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Quiz)