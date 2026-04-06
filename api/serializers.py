from rest_framework import serializers

from catalog.models import Game


class GameSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    categories = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Game
        fields = (
            'id',
            'title',
            'description',
            'min_players',
            'max_players',
            'created_at',
            'owner_username',
            'categories',
        )
