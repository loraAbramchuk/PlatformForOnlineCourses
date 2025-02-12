from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from main.models import Certificate

@receiver(post_save, sender=Certificate)
def certificate_created(sender, instance, created, **kwargs):
    if created:  # Проверяем, что сертификат только что создан
        print(f"🎉 Сертификат для {instance.user.username} по курсу '{instance.course.title}' успешно создан!")  # Вывод в консоль
