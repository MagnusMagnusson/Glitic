from django.test import Client
import hashlib
import json
import secrets
import random

class GameClient(Client):
    ctoken = None 
    stoken = None
    game = None 

    def connect(self, game, secret):
        gid = game.id 
        pre = secret.prefix
        post = secret.suffix 
        token = secrets.token_urlsafe(8)[:8]
        hash = hashlib.sha1()
        hash.update(token.encode("utf-8") + post.encode("utf-8"))
        url = "/api/game/"+gid+"/connect/"
        r = self.post(url, data = {
            "key" : pre,
            "token": token,
            "hash" : hash.hexdigest(),
            "encoding":"sha1"
        })
        if r.status_code == 200:
            self.ctoken = token 
            cont = json.loads(r.content)
            self.stoken = cont["token"]
            self.game = cont["game"]
        return r

    def disconnect(self):
        g = self.game["id"]
        url = "/api/game/"+str(g)+"/disconnect/"
        r = self.post(url, data = {
            "token" : self.stoken
        })
        return r

    def prepheaders(self, data):
        hash = hashlib.sha1()
        imp = secrets.token_hex(5)
        hash.update(data.encode('utf-8'))
        hash.update(imp.encode("utf-8"))     
        hash.update(self.ctoken.encode("utf-8"))
        extra = {
            "HTTP_X_TOKEN" : self.stoken,
            "HTTP_X_IMP" : imp,
            "HTTP_X_CHECKSUM" : hash.hexdigest(),
        }
        return extra

    def post(self, *args, **kwargs):
        if self.stoken:
            data = kwargs["data"]
            extra = self.prepheaders(json.dumps(data))
            return super(Client, self).post(content_type ='application/json', *args, **kwargs, **extra)
        else:
            return super(Client,self).post(content_type ='application/json',*args,**kwargs)