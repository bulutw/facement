from django.contrib import admin
from .models import Card, Item, CardHolder, PayHolder, CustomUser

admin.site.register(Card)
admin.site.register(Item)
admin.site.register(CardHolder)
admin.site.register(PayHolder)
admin.site.register(CustomUser)