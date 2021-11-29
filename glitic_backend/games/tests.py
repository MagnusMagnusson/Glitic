from django.test import TestCase
from glitic_backend.util.gameclient import GameClient
from games.models import Game
from django.contrib.auth.models import User
from clientkeys.models import Clientkey, ClientToken
import hashlib
import secrets


class GameTestCase(TestCase):
    def setUp(self):
        g = Game.objects.create(
            name = "ConnectionTestGame"
        )
        Clientkey.objects.create(
            game = g,
            name = "ConnectionTestKey"
        )

    def test_connect_disconnect(self):
        c = GameClient()
        secret = Clientkey.objects.get(name = "ConnectionTestKey")
        game = Game.objects.get(name="ConnectionTestGame")
        self.assertEqual(secret.game, game, "secret key game does not match intended game")

        client = GameClient()
        r = client.connect(game, secret)
        self.assertEqual(r.status_code, 200, "connect: Connection returne non-200 : <"+ str(r.status_code)+"> " + str(r.content))
        self.assertTrue(ClientToken.objects.filter(servertoken = client.stoken, clienttoken = client.ctoken).exists(), "Token matching recently created connection credentials not found")

        r = client.disconnect()
        self.assertEqual(r.status_code, 200, "disconnect: Connection returned non-200 : <"+ str(r.status_code)+"> " + str(r.content))
        self.assertFalse(ClientToken.objects.filter(servertoken = client.stoken, clienttoken = client.ctoken).exists(), "Token matching recently created connection credentials not found")
