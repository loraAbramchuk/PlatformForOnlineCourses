from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    completed_courses = models.ManyToManyField('main.Course', blank=True)
