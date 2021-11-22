from rest_framework import serializers
from games.models import Game
from highscores.serializers import SimpleTableSerializer

class GameSerializer(serializers.ModelSerializer):
    tables = SimpleTableSerializer(many = True, read_only = True, source='simpletable_set')
    class Meta:
        model = Game 
        fields = ['id', 'tables', 'name', 'shortName']