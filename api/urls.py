from django.urls import path

from .views import GameDetailAPIView, GameListAPIView, PingView

urlpatterns = [
    path('ping/', PingView.as_view(), name='api-ping'),
    path('games/', GameListAPIView.as_view(), name='api-game-list'),
    path('games/<int:pk>/', GameDetailAPIView.as_view(), name='api-game-detail'),
]
