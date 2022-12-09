from django.apps import AppConfig


class UzytkownicyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uzytkownicy'

    def ready(self):
        import uzytkownicy.signals