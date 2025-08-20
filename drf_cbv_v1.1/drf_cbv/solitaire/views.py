from .models import Card,Deck,DeckCard
from django.db import models
from .serializers import DeckSerializer,CardSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from django.db.models import Q

@api_view(['GET', 'POST'])
def decks_list(request):
    SUIT_CHOICES = ["hearts", "diamonds", "clubs", "spades"]
    RANK_CHOICES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    if request.method == 'GET':
        min_cards = request.query_params.get('min_cards')
        max_cards = request.query_params.get('max_cards')
        if min_cards is not None or max_cards is not None:
          if min_cards is None:
              max_cards = int(max_cards)
              deck = Deck.objects.annotate(num=models.Count('cards'))
              deck=deck.filter(num__lte=max_cards)
              serializer = DeckSerializer(deck,many=True)
              if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          elif max_cards is None:
              min_cards = int(min_cards)
              deck = Deck.objects.annotate(num=models.Count('cards'))
              deck = deck.filter(num__gte=min_cards)
              serializer = DeckSerializer(deck, many=True)
              if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          else:
              min_cards = int(min_cards)
              max_cards = int(max_cards)
              deck = Deck.objects.annotate(num=models.Count('cards'))
              deck = deck.filter(Q(num__gte=min_cards) & Q(num__lte=max_cards))
              serializer = DeckSerializer(deck, many=True)
              if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            deck = Deck.objects.all()
            serializer = DeckSerializer(deck, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        cards = request.data.get('cards')
        if cards:
            deck = Deck.objects.create()
            for card in cards:
                card2 = Card.objects.create(suit=card['suit'], rank=card['rank'])
                deck.add_card(card2)
            serializer = DeckSerializer(deck, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            deck = Deck.objects.create()
            for suit in SUIT_CHOICES:
                for rank in RANK_CHOICES:
                    card = Card.objects.get_or_create(suit=suit, rank=rank)[0]
                    deck.add_card(card)
            serializer = DeckSerializer(deck,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def shuffle_deck(request,deck_id):
    if request.method == 'POST':
        try:
            deck = Deck.objects.get(pk=deck_id)
        except Deck.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        deck.shuffle_deck()
        deck.save()
        serializer = DeckSerializer(deck,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        deck = Deck.objects.get(pk=deck_id)
        deck.shuffle_deck()
        deck.save()
        serializer = DeckSerializer(deck)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeckListView(APIView):
    def get(self,request, format=None):
        min_cards = request.query_params.get('min_cards')
        max_cards = request.query_params.get('max_cards')
        if min_cards is not None or max_cards is not None:
            if min_cards is None:
                max_cards = int(max_cards)
                deck = Deck.objects.annotate(num=models.Count('cards'))
                deck = deck.filter(num__lte=max_cards)
                serializer = DeckSerializer(deck, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif max_cards is None:
                min_cards = int(min_cards)
                deck = Deck.objects.annotate(num=models.Count('cards'))
                deck = deck.filter(num__gte=min_cards)
                serializer = DeckSerializer(deck, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                min_cards = int(min_cards)
                max_cards = int(max_cards)
                deck = Deck.objects.annotate(num=models.Count('cards'))
                deck = deck.filter(Q(num__gte=min_cards) & Q(num__lte=max_cards))
                serializer = DeckSerializer(deck, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            deck = Deck.objects.all()
            serializer = DeckSerializer(deck, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        SUIT_CHOICES = ["hearts", "diamonds", "clubs", "spades"]
        RANK_CHOICES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        cards = request.data.get('cards')
        if cards:
            deck = Deck.objects.create()
            for card in cards:
                card2 = Card.objects.create(suit=card['suit'], rank=card['rank'])
                deck.add_card(card2)
            serializer = DeckSerializer(deck, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            deck = Deck.objects.create()
            for suit in SUIT_CHOICES:
                for rank in RANK_CHOICES:
                    card = Card.objects.get_or_create(suit=suit, rank=rank)[0]
                    deck.add_card(card)
            serializer = DeckSerializer(deck, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShuffleDeckView(APIView):
    def get(self,request,deck_id,format=None):
        deck = Deck.objects.get(pk=deck_id)
        deck.shuffle_deck()
        deck.save()
        serializer = DeckSerializer(deck)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,deck_id,format=None):
        try:
            deck = Deck.objects.get(pk=deck_id)
        except Deck.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        deck.shuffle_deck()
        deck.save()
        serializer = DeckSerializer(deck, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeckDetailView(APIView):
    def get(self,request,deck_id,format=None):
        try:
            deck = Deck.objects.get(pk=deck_id)
        except Deck.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=DeckSerializer(deck,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CardList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Card.objects.all()
    serializer_class =CardSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CardDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Card.objects.all()
    serializer_class =CardSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
