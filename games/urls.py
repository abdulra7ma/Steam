from django.urls import path, include
from .views import GameListView

urlpatterns = [
    path('list-game/', GameListView.as_view())
]
