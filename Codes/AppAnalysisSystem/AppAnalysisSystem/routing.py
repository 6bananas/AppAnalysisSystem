from django.urls import path
from .consumers import ProgressConsumer

websocket_urlpatterns = [
    path('progress', ProgressConsumer.as_asgi()),
]