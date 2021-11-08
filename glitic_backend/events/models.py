from glitic_backend.util.urimodel import UriModel
from django.db import models
from games.models import Game
from datetime import date
from django.utils import timezone
import random


class Event(UriModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    label = models.CharField(max_length=64)
    cumulative = models.BooleanField(default = True)
    time_split = models.BooleanField(default = True)
    randsamp = models.IntegerField(default = 1)

    @staticmethod
    def register(game, label, note, info = ""):
        ev = None
        try:
            ev = Event.objects.get(game = game, label = label)
        except Event.DoesNotExist as ex:
            return False
        ev.inc(note, info)

    def inc(self,note, info):            
        today = timezone.make_aware(date.today())
        ec = self.eventcounter_set.objects.latest("date")
        if not ec:                
            ec = Eventcounter(
                event = self,
                date = today
            )
            ec.save()
        if self.time_split:
            if not (today == ec.date):
                ec = Eventcounter(
                    event = self,
                    date = today
                )
                ec.save()
        if self.cumulative:
            ec.inc(note)
        else:
            ec.log(note, info, self.randsamp)

    def __str__(self):
        return str(self.game) + " [ " + self.label + " ] "
            

        
class Eventcounter(UriModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField(auto_now = True)

    def inc(self, note):
        en = self.eventnote_set.filter(note = note)
        if not en.exists():
            en = Eventnote(
                eventcounter = self,
                note = note,
                counter = 1
            )
            en.save()
        else:
            en = en[0]
            en.counter = en.counter + 1
            en.save()

    def log(self, note, info, randsamp = 1):
        self.inc(note)
        if randsamp > 1:
            if random.randint(0, randsamp - 1) != 0:
                return

        er = Eventregister(
            event = self,
            note = note,
            info = info
        )
        er.save()


class Eventnote(UriModel):
    counter = models.ForeignKey(Eventcounter, on_delete=models.CASCADE)
    note = models.CharField(max_length=64, default = "", blank = True)
    value = models.IntegerField(default = 0)


class Eventregister(UriModel):
    counter = models.ForeignKey(Eventcounter, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now = True)
    note = models.CharField(max_length = 64, default ="", blank = True)
    info = models.TextField(max_length=1024)
    