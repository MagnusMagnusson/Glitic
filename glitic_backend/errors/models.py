from django.db import models
from django.db.models.fields.related import ForeignKey
from games.models import Game

class Error(models.Model):
    game = ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    info = models.TextField(max_length = 2048)
    reporter = models.CharField(max_length=32)
    cleared = models.BooleanField(default = False )

    def __str__(self):
        return "Error "+id+" @ " + str(self.game)