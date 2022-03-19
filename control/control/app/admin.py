from django.contrib import admin
from .models import MobileUser, Card, Client, Process

admin.site.register(MobileUser)
admin.site.register(Card)
admin.site.register(Client)
admin.site.register(Process)