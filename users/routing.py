
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("notifications/", consumers.NotificationsConsumer.as_asgi()),
]