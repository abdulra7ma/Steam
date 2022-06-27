from dataclasses import fields
from rest_framework import serializers
from .models import Game


class GameListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'

    