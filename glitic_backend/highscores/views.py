import json
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes
from clientkeys.permissions import ClientKeyChecksumMatch
from highscores.models import Simpletable, Simplescore

class HighscoreViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        perm = super().get_permissions()
        if self.action != 'connect':
            perm.append(ClientKeyChecksumMatch)
        return perm

    def list(self, request):
        
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)