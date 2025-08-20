from django.db import models


class Game(models.Model):
    # Возможные варианты жанра
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('rpg', 'RPG'),
        ('strategy', 'Strategy'),
        ('simulation', 'Simulation'),
        ('adventure', 'Adventure'),
        ('puzzle', 'Puzzle'),
    ]

    # Возможные варианты для платформы
    PLATFORM_CHOICES = [
        ('pc', 'PC'),
        ('xbox', 'Xbox'),
        ('playstation', 'PlayStation'),
        ('switch', 'Nintendo Switch'),
        ('mobile', 'Mobile'),
    ]

    # Возможные варианты для рейтинга
    RATING_CHOICES = [
        (1.0, '1.0'),
        (1.5, '1.5'),
        (2.0, '2.0'),
        (2.5, '2.5'),
        (3.0, '3.0'),
        (3.5, '3.5'),
        (4.0, '4.0'),
        (4.5, '4.5'),
        (5.0, '5.0'),
    ]

    title = models.CharField(max_length=255)  # Название игры
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)  # Жанр игры
    publisher = models.CharField(max_length=255)  # Издатель игры
    release_date = models.DateField()  # Дата выхода игры
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена игры
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES)  # Платформа
    description = models.TextField(blank=True, null=True)  # Описание игры
    rating = models.FloatField(choices=RATING_CHOICES, blank=True, null=True)  # Рейтинг игры
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления записи

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return self.title
