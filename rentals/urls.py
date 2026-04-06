from django.urls import path

from .views import (
    IncomingRentalRequestListView,
    MyRentalRequestListView,
    RentalCancelView,
    RentalDecisionView,
    RentalRequestCreateView,
    RentalRequestDetailView,
)

app_name = 'rentals'

urlpatterns = [
    path('games/<int:game_pk>/request/', RentalRequestCreateView.as_view(), name='request-create'),
    path('my/', MyRentalRequestListView.as_view(), name='my-requests'),
    path('incoming/', IncomingRentalRequestListView.as_view(), name='incoming-requests'),
    path('<int:pk>/', RentalRequestDetailView.as_view(), name='request-detail'),
    path('<int:pk>/cancel/', RentalCancelView.as_view(), name='request-cancel'),
    path('<int:pk>/decide/', RentalDecisionView.as_view(), name='request-decide'),
]
