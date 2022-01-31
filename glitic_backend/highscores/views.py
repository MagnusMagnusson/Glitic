from django.core.exceptions import FieldError, PermissionDenied
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.utils import NotSupportedError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from clientkeys.permissions import  ClientKeyOrOwner
from highscores.models import Simpletable
from highscores.serializers import SimpleTableSerializer, SimplescoreSerializer
from glitic_backend.util.filter import DetailedCompleteFilter
from glitic_backend.util.get_ip import get_client_ip
from glitic_backend.secret import database_allows_distinct_on


class HighscoreViewSet(viewsets.ViewSet):
    filterset_fields = ['primary']    
    order_field = ['primary','secondary','date', 'username', 'userid', 'label']
    def retrieve(self, request, pk=None):
        table = get_object_or_404(Simpletable, pk=pk)
        if not ClientKeyOrOwner(request, self, table.game):
            raise PermissionDenied

        return JsonResponse(SimpleTableSerializer(table).data)

    @action(methods=["GET","POST"], detail = True)
    def scores(self, request, pk=None):        
        if request.method == "GET":
            return self.scores_get(request, pk)
        elif request.method == "POST":
            return self.scores_post(request, pk)

    def scores_get(self,request,pk = None):
        table = get_object_or_404(Simpletable, pk=pk)
        if not ClientKeyOrOwner(request, self, table.game):
            raise PermissionDenied

        scores = table.simplescore_set.all()
        
        f = request.GET
        page = 0
        pSize = 25  
        order = [
            '-primary' if table.ascending_primary else 'primary',
            '-secondary' if table.ascending_secondary else 'secondary'
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
                    print("oredering by "+field)
                    order.append(field)

        scores = DetailedCompleteFilter().filter_queryset(request, scores, self)
        scores = scores.order_by(*order)


        if database_allows_distinct_on and 'user_unique' in f:
            scores = scores.distinct('userid')

        scores = scores[page * pSize : (page + 1) * pSize]

        data = SimplescoreSerializer(scores,many=True).data
        return Response(data)
       
    
    def scores_post(self, request, pk = None):        
        table = get_object_or_404(Simpletable, pk=pk)
        if not ClientKeyOrOwner(request, self, table.game):
            raise PermissionDenied

        scores = table.simplescore_set.all()
        data = request.data 

        SimplescoreSerializer.validate(data)
        
        if table.user_unique:
            pass
        else:
            attempt = table.add(data)
