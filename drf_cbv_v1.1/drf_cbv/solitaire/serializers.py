from rest_framework import serializers
from .models import Card,Deck,DeckCard

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields ='__all__'

class DeckSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    class Meta:
        model = Deck
        fields = ['id','cards']

    def get_cards(self,obj):
        set =  obj.cards.all()
        cards = CardSerializer(set,many = True).data
        return cards