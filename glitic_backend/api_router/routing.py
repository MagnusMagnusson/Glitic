from django.db import router
from django.db.models import base
from rest_framework import routers
from games.views import GameViewSet

router = routers.DefaultRouter()

games = router.register("game", GameViewSet, basename="game")

urlpatterns = router.urls