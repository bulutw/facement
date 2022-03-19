from rest_framework import serializers
from .models import CardHolder, PayHolder

class CardHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardHolder
        fields = ['process_id', 'success']

class PayHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayHolder
        fields = ['unq_id', 'confirm']