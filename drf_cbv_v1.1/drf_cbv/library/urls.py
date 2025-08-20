from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from library import views

urlpatterns = [
    path('games/', views.GameList.as_view()),
    path('games/<int:pk>/', views.GameDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)