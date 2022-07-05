from http import server
from requests import Response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from .serializers import GameSerializer, GameListSerializer
from games.models import Game, Favorite
from rest_framework.decorators import action
from rest_framework import permissions
# from rest_framework import status
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers




class GameListView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameListSerializer
    permission_classes = [permissions.IsAuthenticated,]   



class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated,]


    def get_permissions(self):
        if self.action == ['create', 'update', 'destroy'] :
            return [permissions.IsAdminUser(),]
        else:
            return [permissions.IsAuthenticated(),]


    def get_queryset(self):
        data =  super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            data = data.filter(Q(title__icontains=search) | Q(category=search))
        return data


        


    # def get_queryset(self):
    #     data = super().get_queryset()
    #     search = self.request.query_params.get("search")
    #     if search:
    #         data = data.filter(Q(title__icontains=search) | Q(category=search))
    #     return data

    
    @action(detail=True, methods=['GET'])
    def favorite(self, request, pk):
        product = self.get_object()
        user = request.user
        fav_obj, created = Favorite.objects.get_or_create(product=product, user=user)
        if fav_obj.favorite == False:
            fav_obj.save()
            return Response('add to favs')

        else:
            fav_obj.favorite = not fav_obj.favorite
            fav_obj.save()
            return Response('removed from favs')



