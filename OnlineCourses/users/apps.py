from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'

    def ready(self):
        print("DEBUG: Инициализация приложения users...")
        from . import signals
        signals.ready()  # Вызываем функцию подключения сигналов
        print("DEBUG: Приложение users инициализировано")