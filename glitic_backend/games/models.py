from glitic_backend.util.urimodel import UriModel
from django.db import models
from django.contrib.auth.models import User

class Game(UriModel):
    name = models.CharField(max_length=64, null=False, blank = False, default = "Game Name")
    shortName = models.CharField(max_length = 16, null=False, blank=True, default = "")
    owners = models.ManyToManyField(User)

    def __str__(self):
        name = self.shortName if self.shortName != "" else self.name
        return name + " - " + self.owners.all()[0].username