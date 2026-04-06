from django.urls import path

from .views import ReviewCreateView, ReviewDeleteView, ReviewDetailView, ReviewListView, ReviewUpdateView

app_name = 'reviews'

urlpatterns = [
    path('', ReviewListView.as_view(), name='review-list'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('games/<int:game_pk>/new/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/edit/', ReviewUpdateView.as_view(), name='review-update'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
