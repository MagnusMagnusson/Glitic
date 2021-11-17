from django.db import models
from games.models import Game
from django.core.exceptions import PermissionDenied
import secrets
import random
from django.utils import timezone
from datetime import datetime, timedelta
import hashlib

class ClientKeyPermission(models.Model):
    code = models.CharField(max_length = 16, primary_key=True)
    name = models.CharField(max_length = 32, unique = True)
    description = models.CharField(max_length = 256)

class Clientkey(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    key = models.CharField(max_length=13, primary_key=True)
    prefix = models.CharField(max_length=4, editable=False)
    suffix = models.CharField(max_length=8, editable=False)
    revoked = models.BooleanField(default = False)
    expired = models.BooleanField(default = False)
    generated = models.DateTimeField(auto_now = True)
    expires = models.DateTimeField(null = True, default = None, blank=True)
    name = models.CharField(blank=False, default="Unnamed Key", max_length=32)
    details = models.TextField(max_length=1024, blank=True)
    permissions = models.ManyToManyField(ClientKeyPermission, blank=True)

    def __init__(self, *args, **kwargs):
        super(Clientkey, self).__init__(*args, **kwargs)
        self.originalKey =  self.key if hasattr(self,"key") else ""
        self.originalGame = self.game if hasattr(self,"game") else None
        self.originalPrefix = self.prefix if hasattr(self,"prefix") else ""
        self.originalSuffix = self.suffix if hasattr(self,"suffix") else ""
    
    def hasChanged(self):
        return (
            self.key != self.originalKey and self.originalKey != "" 
            and self.originalGame != self.game and self.originalGame != None
            and self.originalPrefix != self.prefix and self.originalPrefix != ""
            and self.originalSuffix != self.suffix and self.originalSuffix != ""
        )
    
    def genkey(self):
        if not (self.originalKey == ""):
            raise PermissionDenied()
        t = "abcdefghijklmnopqrstuvwxyz1234567890"
        p = secrets.token_urlsafe(4)[:4].replace("-",t[random.randint(0,36)]).replace("_",t[random.randint(0,36)])
        s = secrets.token_urlsafe(8)[:8].replace("-",t[random.randint(0,36)]).replace("_",t[random.randint(0,36)])
        cand = Clientkey.objects.filter(prefix = p, suffix = s).exists()
        while cand:
            p = secrets.token_urlsafe(32)[:4].replace("-",t[random.randint(0,36)]).replace("_",t[random.randint(0,36)])
            s = secrets.token_urlsafe(32)[:8].replace("-",t[random.randint(0,36)]).replace("_",t[random.randint(0,36)])
            cand = Clientkey.objects.filter(prefix = p, suffix = s).exists()
        self.prefix = p 
        self.suffix = s
        self.key = self.prefix + "-" + self.suffix

    def save(self):
        if(self.revoked or self.expired):
            raise PermissionDenied()
        if self.hasChanged():
            raise PermissionDenied()
        if self.originalKey == "":
            self.genkey()
        super(Clientkey, self).save()

    def hasPermission(self, permission):
        return self.clientkeypermission_set.filter(code = permission).exists()
    
    @staticmethod 
    def GenerateKey(game, name = None, expires = None, details = None):
        key = Clientkey(
            game = game, 
            expires = expires,
            details = details
        )
        key.save()
        return key

    def GenerateToken(self, cToken, encoding):
        t = ClientToken()
        token = secrets.token_urlsafe(8)[:8]
        while ClientToken.objects.filter(servertoken = token).exists():
            token = secrets.token_urlsafe(8)[:8]
        t.servertoken = token 
        t.clienttoken = cToken
        t.encoding = encoding
        t.key = self
        t.save()
        return t

    def isValid(self):
        return not (self.revoked or self.expired)
            

class ClientToken(models.Model):
    servertoken = models.CharField(max_length=16, primary_key=True)
    clienttoken = models.CharField(max_length=16)
    key = models.ForeignKey(Clientkey, on_delete=models.CASCADE)
    encoding = models.CharField(max_length=10, default="sha1")

    last_active = models.DateTimeField(auto_now=True)

    def expired(self):
        if self.last_active + timedelta(hours = 6) < timezone.make_aware(datetime.now()):
            self.delete()
            return True
        return False


    def ping(self):
        self.last_active = timezone.now()
        self.save()

    def getHashObject(self):
            enc = self.encoding
            if enc == "sha256":
                test = hashlib.sha256()
            elif enc == "sha224":
                test = hashlib.sha224()
            elif enc == "sha384":
                test = hashlib.sha384()
            elif enc == "sha512":
                test = hashlib.sha512()
            elif enc == "md5":
                test = hashlib.md5()
            else:
                test = hashlib.sha1()
            return test