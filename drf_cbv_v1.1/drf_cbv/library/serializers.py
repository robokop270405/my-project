from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    publisher = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'title', 'genre', 'publisher', 'release_date', 'price', 'platform', 'description', 'rating', 'created_at', 'updated_at']

    def validate_price(self, value):
        """
        Проверяет, чтобы цена была больше нуля.
        """
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля.")
        return value

    def validate(self, data):
        """
        Проверяет, что рейтинг, если указан, находится в допустимом диапазоне.
        """
        rating = data.get('rating')
        if rating is not None and (rating < 1.0 or rating > 5.0):
            raise serializers.ValidationError("Рейтинг должен быть в диапазоне от 1.0 до 5.0 c шагом 0.5.")
        return data