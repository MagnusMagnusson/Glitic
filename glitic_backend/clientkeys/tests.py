from django.test import TestCase
from glitic_backend.util.gameclient import GameClient
from games.models import Game
from django.contrib.auth.models import User
from clientkeys.models import Clientkey, ClientToken
import hashlib
import secrets


class ClientkeySecurityTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create(
            username = "User_Clientkeysectest_1",
        )
        g1 = Game.objects.create(
            name = "Game_Clientkeysectest_1"
        )
        g1.owners.add(u1)
        Clientkey.objects.create(
            game = g1,
            name = "Clientkey_Clientkeysectest_1"
        )
        u2 = User.objects.create(
            username = "User_Clientkeysectest_2",
        )
        g2 = Game.objects.create(
            name = "Game_Clientkeysectest_2"
        )
        g2.owners.add(u2)
        Clientkey.objects.create(
            game = g2,
            name = "Clientkey_Clientkeysectest_2"
        )

    def test_failed_connection(self):
        c = GameClient()
        secret = Clientkey.objects.get(name = "Clientkey_Clientkeysectest_1")
        game = Game.objects.get(name="Game_Clientkeysectest_1")

        

        
