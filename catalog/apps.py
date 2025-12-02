from django.apps import AppConfig

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        """Автоматически создаёт суперпользователя Simba (пароль simba123)"""
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError, ProgrammingError

        User = get_user_model()
        try:
            if not User.objects.filter(username='Simba').exists():
                User.objects.create_superuser(
                    username='Simba',
                    email='',
                    password='simba123'
                )
                print("✅ Создан суперпользователь Simba (пароль: simba123)")
        except (OperationalError, ProgrammingError):
            # Пропускаем, если база данных ещё не готова
            pass
