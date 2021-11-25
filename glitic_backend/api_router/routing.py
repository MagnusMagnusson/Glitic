from django.db import router
from django.db.models import base
from rest_framework import routers
from games.views import GameViewSet
from highscores.views import HighscoreViewSet

router = routers.DefaultRouter()

router.register("game", GameViewSet, basename="game")
router.register("highscore", HighscoreViewSet, basename="highscores")

urlpatterns = router.urls