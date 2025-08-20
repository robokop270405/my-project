from django.db import models
import random
class Card(models.Model):
    SUIT_CHOICES = [("hearts","hearts"),("diamonds","diamonds"),("clubs","clubs"),("spades","spades")]
    RANK_CHOICES = [("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),("10","10"),("J","J"),("Q","Q"),("K","K"),("A","A")]

    suit = models.CharField(choices=SUIT_CHOICES)
    rank = models.CharField(choices= RANK_CHOICES)
    is_face_up = models.BooleanField(default=False)

    class Meta:
        unique_together = [('suit','rank')]

class Deck(models.Model):
    cards = models.ManyToManyField(Card, through='DeckCard')

    def add_card(self,card):
        max_position = self.deck_card.aggregate(max_position=models.Max('position'))['max_position']
        if max_position is None:
             new_position = 0
        else:
             new_position = max_position + 1
        DeckCard.objects.create(deck=self, card=card, position=new_position)
    def shuffle_deck(self):
        positions = list(self.deck_card.all().values_list('position'))
        random.shuffle(positions)
        for i, pos in enumerate(positions):
            DeckCard.objects.update(deck=self,card=self.cards.all()[i],position=pos[0])

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck,on_delete=models.CASCADE,related_name='deck_card')
    card = models.ForeignKey(Card,on_delete=models.CASCADE)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']
