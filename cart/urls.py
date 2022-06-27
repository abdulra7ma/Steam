from django.urls import path
from .views import AddItem

urlpatterns =[
    path('add/', AddItem.as_view())
]