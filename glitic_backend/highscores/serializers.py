from rest_framework import serializers
from highscores.models import Simpletable

class SimpleTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simpletable 
        fields = ['id', 'name', 'user_unique', 'ascending_secondary', 'ascending_primary']