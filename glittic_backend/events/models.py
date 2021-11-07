from glittic_backend.util.urimodel import UriModel
from django.db import models
from games.models import Game


class Event(UriModel):
    id = models.CharField(max_length=10, primary_key=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game)
    label = models.CharField(max_length=64)
    cumulative = models.BooleanField(default = True)
    time_split = models.BooleanField(default = True)
    exact = models.BooleanField(default = False)


class Eventcounter(UriModel):
    id = models.CharField(max_length=10, primary_key=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField(auto_now = True)
    count = models.IntegerField(default = 0)