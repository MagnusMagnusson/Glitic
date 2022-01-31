from glitic_backend.util.get_ip import get_client_ip
from glitic_backend.util.urimodel import UriModel
from django.db import models
from django.db.models.fields.related import ForeignKey
from games.models import Game


class Simpletable(UriModel):
    name = models.CharField(max_length=64)
    game = ForeignKey(Game, on_delete=models.CASCADE, null=False)
    ascending_primary = models.BooleanField(default = True)
    ascending_secondary = models.BooleanField(default = True)
    user_unique = models.BooleanField(default = True) 

    class Meta:
        verbose_name = 'Simple Highscore Table'
        verbose_name_plural = 'Simple Highscore Tables'

    def add(self, primary, secondary, label, username, userid, clientid, ip):
        score = Simplescore(
            table = self,
            primary = primary,
            secondary = secondary,
            label = label,
            username = username,
            userid = userid,
            clientid = clientid,
            ip = ip
        )
        score.save()
        return score
    
    def add(self, request, data):
        ip = get_client_ip(request)
        clientid = request.META['clid']
        return self.add(data['primary'], data['secondary'], data['label'], data['username'], data['userid'], clientid, ip)

    def clear(self):
        self.Simplescore_set.delete()

    def results(self, p, n):
        scores = self.Simplescore_set.order_by( '-primary' if self.ascending_primary else 'primary','-secondary' if self.ascending_secondary else 'secondary')
        return scores[p * n : (p+1) * n]

    def __str__(self):
        return str(self.game) + " : " + self.name

class Simplescore(models.Model):    
    table = ForeignKey(Simpletable, on_delete=models.CASCADE, null=False)
    primary = models.FloatField()
    secondary = models.FloatField()
    label = models.CharField(max_length=16, blank=True)
    date = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=128)
    userid = models.CharField(max_length=128)
    debug = models.BooleanField(default = False)
    clientid = models.CharField(max_length=16, null=False, default="N/A")
    ip = models.GenericIPAddressField()

        
    class Meta:
        verbose_name = 'Simple Highscore Entry'
        verbose_name_plural = 'Simple Highscore Entries'

    def __str__(self):
        return str(self.table) + " " +self.label + " (" + str(self.primary) + ", " + str(self.secondary) +", " + self.username+ ")"
