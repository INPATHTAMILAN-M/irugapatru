from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<slug>\w+)/$", consumers.QuizConsumer.as_asgi()),
]