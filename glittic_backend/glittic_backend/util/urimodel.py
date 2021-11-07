from django.db import models
import secrets

class UriModel(models.Model):
    id = models.CharField(max_length=10, primary_key=True, on_delete=models.CASCADE)

    def save(self):
        if not hasattr(self, "id") or not self.id or self.id == None:
            tid = secrets.token_urlsafe(10)
            cand = __class__.objects.filter(id = tid).exists()
            while cand:
                tid = secrets.token_urlsafe(10)
                cand = __class__.objects.filter(id = tid).exists()
            self.id = tid
        super(models.Model).save()