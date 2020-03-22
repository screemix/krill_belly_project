from django.urls import path
from . import views

urlpatterns = [
    path('articles', views.articles, name='mat_articles'),
    path('podcasts', views.podcasts, name='mat_podcasts'),
]