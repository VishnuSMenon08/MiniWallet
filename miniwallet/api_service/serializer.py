from rest_framework import serializers
from .models import Account, Transaction

class TokenSerializer(serializers.Serializer):
    token_id = serializers.CharField(max_length=50)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','owned_by','status','changed_at','balance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id','transaction_by','transaction_time','amount','reference_id']


