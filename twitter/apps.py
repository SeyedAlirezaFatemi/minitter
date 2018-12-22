from django.apps import AppConfig


class TwitterConfig(AppConfig):
    name = 'twitter'

    def ready(self):
        # Important, Don't remove!
        from twitter import signals
