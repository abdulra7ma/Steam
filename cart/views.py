from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import OrderSerialzier, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated

class AddItem(CreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, ]