from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('cardholders', views.CardHolderViewSet)
router.register('payholders', views.PayHolderViewSet)

urlpatterns = [
    path('login', views.LoginView),
    path('register', views.RegisterView),
    path('marketplace', views.MarketPlace),
    path('', include(router.urls)),
    path('add-card', views.AddCard),
    path('facement', views.Facement),
    path('pay', views.Pay),
    path('add_to_cart/<pk>', views.AddToCart, name = "name?=add_to_cart")
]
