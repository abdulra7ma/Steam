from rest_framework import serializers
from . models import Order, OrderItem

class OrderSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['owner', 'items']


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'date_added']