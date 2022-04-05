from django.apps import AppConfig


class ChatsConfig(AppConfig):
    name = 'chats'

    def ready(selfself):
        import chats.signals