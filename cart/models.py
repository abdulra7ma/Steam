from django.db import models
from games.models import Game
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderItem(models.Model):
    product = models.OneToOneField(Game, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=1)



    def __str__(self) -> str:
        return self.product.title


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

