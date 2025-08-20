# ДЗ4: Представления на основе классов в Django REST Framework

## 1. Переписывание существующих представлений с использованием <code>APIView</code>

Перепишите следующие представления, ранее реализованные как функции, в классовые представления на основе APIView:

* <code>DeckListView</code> (заменяет <code>decks_list</code>):
    * <code>GET</code>-запрос возвращает список колод, поддерживающих фильтрацию по <code>min_cards</code> и <code>max_cards</code> через <code>request.query_params</code>.
    * <code>POST</code>-запрос создает новую колоду. Если в <code>request.data</code> передан список <code>cards</code>, то используется он. Иначе создается стандартная колода из 52 карт.
* <code>ShuffleDeckView</code> (заменяет <code>shuffle_deck</code>):
    * <code>POST</code>-запрос с <code>deck_id</code> перетасовывает указанную колоду и возвращает ее сериализованное представление.
    * Если колода с таким <code>deck_id</code> не существует, возвращается статус <code>404</code>.

Добавьте новое представление <code>DeckDetailView</code> для получения информации о конкретной колоде (<code>GET</code>-запрос). Если колоды нет, возвращается <code>404</code>.

Обновите маршруты в <code>solitaire/urls.py</code>, чтобы использовать новые классовые представления:

* <code>GET</code> <code>/decks/</code> и <code>POST</code> <code>/decks/</code> → <code>DeckListView</code>
* <code>POST</code> <code>/decks/{deck_id}/shuffle/</code> → <code>ShuffleDeckView</code>
* <code>GET</code> <code>/decks/{deck_id}/</code> → <code>DeckDetailView</code>

## 2. Использование миксинов для представлений <code>Card</code>

Создайте представления для модели <code>Card</code> с использованием DRF mixins:

* <code>CardList</code>: использует <code>ListModelMixin</code> и <code>CreateModelMixin</code> и наследуется от <code>GenericAPIView</code> (или <code>Mixin</code> + <code>GenericViewSet</code>).
    * <code>GET</code> → список всех карт
    * <code>POST</code> → создание новой карты
* <code>CardDetail</code>: использует <code>RetrieveModelMixin</code>, <code>UpdateModelMixin</code>, <code>DestroyModelMixin</code> и наследуется от <code>GenericAPIView</code> (или <code>Mixin</code> + <code>GenericViewSet</code>).
    * <code>GET</code> → детальный просмотр карты
    * <code>PUT/PATCH</code> → обновление карты
    * <code>DELETE</code> → удаление карты
    
Обновите маршруты:

* <code>GET</code> <code>/cards/</code>, <code>POST</code> <code>/cards/</code> → <code>CardList</code>
* <code>GET</code> <code>/cards/{card_id}/</code>, <code>PUT/PATCH</code> <code>/cards/{card_id}/</code>, <code>DELETE</code> <code>/cards/{card_id}/</code> → <code>CardDetail</code>

## 3. Все представления должны поддерживать различные форматы (например, JSON), и использовать <code>Response</code> из DRF
