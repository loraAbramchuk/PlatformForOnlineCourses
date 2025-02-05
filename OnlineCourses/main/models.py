from django.db import models
from django.db.models import Model
from django.conf import settings


# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # image = models.ImageField(upload_to='courses/', blank=True, null=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    question = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question

    def get_shuffled_answers(self):
        """Генерируем список ответов, перемешивая варианты"""
        from random import shuffle
        answers = [self.correct_answer, "Неправильный ответ 1", "Неправильный ответ 2"]
        shuffle(answers)
        return answers