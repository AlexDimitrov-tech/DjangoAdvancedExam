from django.urls import path

from .views import (
	CategoryCreateView,
	CategoryDeleteView,
	CategoryDetailView,
	CategoryListView,
	CategoryUpdateView,
    GameCreateView,
    GameDeleteView,
    GameDetailView,
    GameListView,
    GameUpdateView,
    ToggleFavoriteView,
)

app_name = 'catalog'

urlpatterns = [
    path('', GameListView.as_view(), name='game-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/new/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('games/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('games/new/', GameCreateView.as_view(), name='game-create'),
	path('games/<int:pk>/edit/', GameUpdateView.as_view(), name='game-update'),
	path('games/<int:pk>/delete/', GameDeleteView.as_view(), name='game-delete'),
	path('games/<int:pk>/favorite/', ToggleFavoriteView.as_view(), name='game-favorite'),
]
