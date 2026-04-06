from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Game

from .serializers import GameSerializer


class PingView(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request):
		return Response({'status': 'ok'})


class GameListAPIView(generics.ListAPIView):
	queryset = Game.objects.select_related('owner').prefetch_related('categories')
	serializer_class = GameSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]


class GameDetailAPIView(generics.RetrieveAPIView):
	queryset = Game.objects.select_related('owner').prefetch_related('categories')
	serializer_class = GameSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
