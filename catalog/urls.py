from django.urls import path

from .views import GameCreateView, GameDetailView, GameListView

app_name = 'catalog'

urlpatterns = [
    path('', GameListView.as_view(), name='game-list'),
    path('games/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('games/new/', GameCreateView.as_view(), name='game-create'),
]
