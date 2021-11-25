import json
from re import I
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from games.serializers import GameSerializer
from games.models import Game
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from clientkeys.models import ClientToken
from clientkeys.permissions import ClientKeyChecksumMatch,IsAuthenticatedOrClientAuthenticted
import hashlib

class GameViewSet(viewsets.ViewSet):
    def list(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied
        queryset = Game.objects.filter(owners = request.user)
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):  
        queryset = Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        if  ClientKeyChecksumMatch.has_permission(request, self) or game.owners.filter(id = request.user.id).exists():
            serializer = GameSerializer(game)
            return Response(serializer.data)
        else:
            raise PermissionDenied

    @action(detail=True, methods=['post'])
    def connect(self, request, pk=None):
        data = request.data
        queryset = Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        key = game.clientkey_set.filter(prefix=data["key"] if 'key' in data else None)
        
        validHash = False
        if len(key) == 1:
            key = key[0]
            if not key.isValid():
                return JsonResponse({"error":"Key revoked or expired"}, status=401)
            
            checksum = data['hash'] if 'hash' in data else None
            test = None
            enc = data['encoding'] if 'encoding' in data else 'sha1'
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

        try:
            test.update(data["token"].encode("utf-8") if 'token' in data else None)
            test.update(key.suffix.encode("utf-8"))
            validHash = test.hexdigest() == checksum
        except TypeError as e: 
            return JsonResponse({"error":"Tokens must be encoded using utf-8"}, status=400)

        if not validHash:
            return JsonResponse({"error":"Failed to verify checksum token"}, status=401)
        else:
            t = key.GenerateToken(data['token'], enc)
            resp = {}
            gameData = GameSerializer(game).data
            return JsonResponse({
                "game" : gameData,
                "token" : t.servertoken
            })

        
    @action(detail=True, methods=['post'])
    def disconnect(self, request, pk=None):       
        if not ClientKeyChecksumMatch.has_permission(request, self):
            raise PermissionDenied
        data = request.data
        if not 'token' in data:
            return JsonResponse({"error":"Missing token"}, status = 400)
        queryset = Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        try:
            token = ClientToken.objects.get(servertoken=data["token"])
        except ClientToken.DoesNotExist:            
            return JsonResponse({"error": "Token does not exist"})

        token.delete()
        return JsonResponse({"token":None})