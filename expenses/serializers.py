from decimal import Decimal

from balances.models import Balance
from django.contrib.auth import get_user_model
from django.db import transaction
from loguru import logger
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Expense, ExpenseSplit

User = get_user_model()


class ExpenseSplitSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ExpenseSplit
        fields = ["id", "user", "split_value"]


class ExpenseSerializer(serializers.ModelSerializer):
    splits = ExpenseSplitSerializer(many=True)

    class Meta:
        model = Expense
        fields = [
            "id",
            "title",
            "created_by",
            "amount",
            "split_type",
            "splits",
        ]
        read_only_fields = ["created_by"]

    def validate(self, data):
        logger.info(data)
        split_type = data.get("split_type")
        splits = data.get("splits")
        logger.info(splits)
        if not splits:
            raise serializers.ValidationError("Participants are required")
        if split_type == "exact":
            total_amount = sum([split["split_value"] for split in splits])
            if total_amount != data.get("amount"):
                raise serializers.ValidationError(
                    "Total amount should match the expense amount"
                )
        elif split_type == "percent":
            total_percent = sum([split["split_value"] for split in splits])
            if total_percent != 100:
                raise serializers.ValidationError("Total percent should be 100")
        return data

    def create(self, validated_data):
        splits_data = validated_data.pop("splits")
        split_type = validated_data.get("split_type")

        with transaction.atomic():
            expense = Expense.objects.create(**validated_data)
            self.handle_splits(expense, splits_data, split_type)

        return expense

    def handle_splits(self, expense, splits_data, split_type):
        for participant in splits_data:
            logger.info(participant)
            user = participant["user"]
            split_value = participant["split_value"]
            if split_type == "percent":
                split_value = (expense.amount * split_value) / 100
            elif split_type == "equal":
                split_value = expense.amount / len(splits_data)
            elif split_type == "exact":
                pass
            ExpenseSplit.objects.create(
                expense=expense,
                user=user,
                split_value=split_value,
            )
            self.update_balances(expense.created_by, user, split_value)

    def update_balances(self, payer, payee, amount):
        if payer == payee:
            return

        user_1, user_2 = (payer, payee) if payer.id < payee.id else (payee, payer)

        balance, _ = Balance.objects.select_for_update().get_or_create(
            user_1=user_1, user_2=user_2
        )

        # Adjust the balance based on the payer and payee
        if payer == user_1:
            balance.balance = Decimal(balance.balance) + amount
        else:
            balance.balance = Decimal(balance.balance) - amount

        balance.save()
