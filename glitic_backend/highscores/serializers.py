from rest_framework import serializers
from highscores.models import Simpletable, Simplescore

class SimpleTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simpletable 
        fields = ['id', 'name', 'user_unique', 'ascending_secondary', 'ascending_primary']

class SimplescoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Simplescore
        fields = ['primary','secondary','date','username','userid']