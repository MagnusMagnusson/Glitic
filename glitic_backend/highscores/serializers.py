from django.core.exceptions import ValidationError
from rest_framework import serializers
from highscores.models import Simpletable, Simplescore

class SimpleTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simpletable 
        fields = ['id', 'name', 'user_unique', 'ascending_secondary', 'ascending_primary']

class SimplescoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simplescore
        fields = ['primary','secondary','date','username','userid', 'label']

    def validate(self, data):
        try:
            if not (
                'primary' in data and
                'secondary' in data and
                'username' in data and
                'userid' in data and
                len(data['username']) <= 128 and
                len(data['userid']) <= 128 
            ):
                raise ValidationError
            else:
                p = float(data['primary']) 
                s = float(data['secondary'])  
                return True
        except ValueError:
            raise ValidationError