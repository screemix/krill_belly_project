from django.urls import path
from . import views

urlpatterns = [
    path('selections', views.selections, name='selections'),
    path('wish_list', views.wish_list, name='wish_list'),
    path('cart', views.cart, name='cart'),
]