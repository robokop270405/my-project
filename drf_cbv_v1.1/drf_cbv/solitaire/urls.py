from django.urls import path
from solitaire import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[

    #path("decks/",views.decks_list,name="deck-list"),
    #path("decks/<deck_id>/shuffle/", views.shuffle_deck, name="shuffle-deck"),
    path("decks/", views.DeckListView.as_view(), name="deck-list"),
    path("decks/<deck_id>/shuffle/", views.ShuffleDeckView.as_view(), name="shuffle-deck"),
    path("decks/<deck_id>/",views.DeckDetailView.as_view(),name='hz'),
    path("cards/",views.CardList.as_view()),
    path("cards/<pk>/",views.CardDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)