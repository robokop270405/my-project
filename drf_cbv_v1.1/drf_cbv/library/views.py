from rest_framework import generics
from .models import Game
from .serializers import GameSerializer


class GameList(generics.ListCreateAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        """
        Переопределяем queryset для фильтрации по определенным условиям.
        """
        queryset = Game.objects.all()
        genre = self.request.query_params.get('genre')
        if genre is not None:
            queryset = queryset.filter(genre=genre)
        return queryset

    def perform_create(self, serializer):
        """
        Дополнительная логика при создании объекта.
        """
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

