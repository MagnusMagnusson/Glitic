from glittic_backend.util.urimodel import UriModel
from django.db import models
from django.db.models.fields.related import ForeignKey
from games.models import Game
import secrets

class Simpletable(UriModel):
    name = models.CharField(max_length=64)
    game = ForeignKey(Game, on_delete=models.CASCADE, null=False)
    ascending_primary = models.BooleanField(default = True)
    ascending_secondary = models.BooleanField(default = True)
    user_unique = models.BooleanField(default = True) 

    def add(self, primary, secondary, label, username, userid):
        score = Simplescore(
            table = self,
            primary_score = primary,
            secondary_score = secondary,
            label = label,
            username = username,
            userid = userid
        )
        score.save()
        return score

    def clear(self):
        self.Simplescore_set.delete()

    def results(self, p, n):
        scores = self.Simplescore_set.order_by( '-primary' if self.ascending_primary else 'primary','-secondary' if self.ascending_secondary else 'secondary')
        return scores[p * n : (p+1) * n]


class Simplescore(models.Model):
    table = ForeignKey(Simpletable, on_delete=models.CASCADE, null=False)
    primary = models.FloatField()
    secondary = models.FloatField()
    label = models.CharField(max_length=16)
    date = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=128)
    userid = models.CharField(max_length=128)
