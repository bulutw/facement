from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import MobileUserViewSet
from .views import MobileLogin, MobileRegister, Add_Card, Check_Card, Receive_Payment

router = routers.DefaultRouter()
router.register('users', MobileUserViewSet)

urlpatterns = [
    path('Q/', include(router.urls)),
    path('mobilelogin/<username>/<password>/<token>', MobileLogin, name = "name?=mobile_login"),
    path('mobileregister/<username>/<password>/<token>', MobileRegister, name = "name?=mobile_register"),
    path('add-card/<cc_number>/<client_id>', Add_Card.as_view(), name = "name?=add_card"),
    path('check-card/<cc_number>', Check_Card.as_view(), name = "name?=check-card"),
    path('payment/<cc_number>', Receive_Payment.as_view(), name="name?=payment"),
]