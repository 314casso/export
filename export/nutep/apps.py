from django.apps import AppConfig
from nutep.signals import connect_signals


class NutepConfig(AppConfig):
    def ready(self):
        connect_signals()