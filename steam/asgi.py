"""
ASGI config for cinema project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),                             #Публичный интерфейс для поддержки ASGI Django. Возвращает вызываемый объект ASGI 3.
                                                                #Не делает django.core.handlers.ASGIHandler общедоступным API, если
                                                                #внутренняя реализация изменяется или перемещается в будущем.
     
    'websocket': AuthMiddlewareStack(#Извлекает файлы cookie из областей в стиле HTTP или WebSocket и добавляет их как
                                    #запись scope["cookies"] в том же формате, что и запрос Django.COOKIES
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})
