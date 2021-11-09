from django.db import models
from django.contrib import admin
import secrets

urilength = 5

class UriModel(models.Model):
    class Meta:
        abstract = True
    id = models.CharField(max_length=10, primary_key=True, editable=False)

    def save(self):
        if not hasattr(self, "id") or not self.id or self.id == None:
            tid = secrets.token_urlsafe(urilength)[:urilength]
            cand = type(self).objects.filter(id = tid).exists()
            while cand:
                tid = secrets.token_urlsafe(urilength)[:urilength]
                cand = type(self).objects.filter(id = tid).exists()
            self.id = tid
        super().save()
