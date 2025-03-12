from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from main.models import Certificate
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import CustomUser
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Certificate)
def certificate_created(sender, instance, created, **kwargs):
    if created:  # Проверяем, что сертификат только что создан
        print(f"🎉 Сертификат для {instance.user.username} по курсу '{instance.course.title}' успешно создан!")  # Вывод в консоль

def send_welcome_email_handler(sender, instance, created, **kwargs):
    """
    Отправляет приветственное письмо новому пользователю и уведомление администратору
    """
    print(f"DEBUG: Сигнал send_welcome_email вызван для пользователя {instance.username}")
    logger.info(f"Сигнал send_welcome_email вызван для пользователя {instance.username}")
    
    if created:
        # Отправляем уведомление администратору
        admin_subject = 'Новый пользователь на платформе!'
        admin_message = f'''На платформе зарегистрировался новый пользователь:
- Имя пользователя: {instance.username}
- Email: {instance.email or 'Не указан'}
- Дата регистрации: {instance.date_joined}

Это автоматическое уведомление.'''

        try:
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],  # Отправляем на админский email
                fail_silently=False,
            )
            print(f"DEBUG: Уведомление администратору отправлено на {settings.EMAIL_HOST_USER}")
            logger.info(f"Уведомление администратору отправлено на {settings.EMAIL_HOST_USER}")
        except Exception as e:
            print(f"DEBUG: Ошибка при отправке уведомления администратору: {str(e)}")
            logger.error(f"Ошибка при отправке уведомления администратору: {str(e)}")

        # Отправляем приветственное письмо пользователю, если указан email
        if instance.email:
            try:
                subject = 'Добро пожаловать на платформу OnlineCourses!'
                message = f'''Здравствуйте, {instance.username}!

Мы рады приветствовать вас на нашей платформе онлайн-курсов.
Теперь вы можете:
- Просматривать доступные курсы
- Записываться на интересующие вас курсы
- Получать сертификаты после завершения обучения

Удачи в обучении!

С уважением,
Команда OnlineCourses'''

                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.email],
                    fail_silently=False,
                )
                print(f"DEBUG: Письмо успешно отправлено на {instance.email}")
                logger.info(f"Письмо успешно отправлено на {instance.email}")
            except Exception as e:
                print(f"DEBUG: Ошибка при отправке письма пользователю: {str(e)}")
                logger.error(f"Ошибка при отправке письма пользователю: {str(e)}")

def ready():
    """
    Подключает сигналы при инициализации приложения
    """
    print("DEBUG: Подключение сигналов...")
    post_save.connect(send_welcome_email_handler, sender=CustomUser)
    print("DEBUG: Сигналы подключены")
