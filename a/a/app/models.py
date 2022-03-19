from django.db import models
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

from django.contrib.auth.models import User

class Card(models.Model):
    card_number = CardNumberField()
    card_exp = CardExpiryField()
    card_sec = SecurityCodeField()
    name_on_card = models.CharField(max_length = 40)

class Item(models.Model):
    name = models.CharField(max_length = 24)
    desc = models.TextField(max_length = 100)
    price = models.PositiveIntegerField()
    item_id = models.CharField(max_length = 999, default = "nan")

class CardHolder(models.Model):
    process_id = models.TextField()
    success = models.BooleanField()

class PayHolder(models.Model):
    unq_id = models.IntegerField()
    confirm = models.CharField(default = "None", max_length = 9)

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    cart = models.TextField(null = True, blank = True)
