from django.apps import AppConfig


class TwitterConfig(AppConfig):
    name = 'twitter'

    def ready(self):
        from twitter import signals
