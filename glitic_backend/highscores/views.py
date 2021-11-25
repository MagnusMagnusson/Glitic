from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from clientkeys.permissions import  ClientKeyOrOwner
from highscores.models import Simpletable
from highscores.serializers import SimpleTableSerializer, SimplescoreSerializer
from glitic_backend.util.filter import DetailedCompleteFilter

class HighscoreViewSet(viewsets.ViewSet):
    filterset_fields = ['primary']    
    order_field = ['primary','secondary','date', 'username', 'userid', 'label']
    def retrieve(self, request, pk=None):
        table = get_object_or_404(Simpletable, pk=pk)
        if not ClientKeyOrOwner(request, self, table.game):
            raise PermissionDenied

        return JsonResponse(SimpleTableSerializer(table).data)

    @action(methods=["GET"], detail = True)
    def scores(self, request, pk=None):        
        table = get_object_or_404(Simpletable, pk=pk)
        if not ClientKeyOrOwner(request, self, table.game):
            raise PermissionDenied

        scores = table.simplescore_set.all()
        
        f = request.GET
        page = 0
        pSize = 25

        order = [
            "-primary",
            '-secondary',
        ]

        if 'page' in f:
            page = int(f['page'])
        if 'pagesize' in f:
            pSize = int(f['pagesize'])
        if 'ordering' in f:
            order = []
            orderingString = f['ordering'].split(",")
            for field in orderingString:
                if field in self.order_field or (field[0] == "-" and field[1:] in self.order_field):
                    print(field)
                    order.append(field)

        scores = DetailedCompleteFilter().filter_queryset(request, scores, self)
        scores = scores.order_by(*order)
        scores = scores[page * pSize : (page + 1) * pSize]
        data = SimplescoreSerializer(scores,many=True).data
        return Response(data)
       