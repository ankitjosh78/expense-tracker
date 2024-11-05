from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from balances.models import Balance

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["id", "payer", "payee", "amount", "created_at"]
        read_only_fields = ["payer"]

    def create(self, validated_data):
        with transaction.atomic():
            transaction_instance = Transaction.objects.create(**validated_data)
            self.update_balances(
                transaction_instance.payer,
                transaction_instance.payee,
                transaction_instance.amount,
            )
            return transaction_instance

    def update_balances(self, payer, payee, amount):
        if payer.id < payee.id:
            user_1, user_2, adjustment = payer, payee, amount
        else:
            user_1, user_2, adjustment = payee, payer, -amount

        balance, _ = Balance.objects.select_for_update().get_or_create(
            user=user_1,
            user2=user_2,
        )
        balance.balance = Decimal(balance.balance) + adjustment
        balance.save()
