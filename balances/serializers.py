from django.contrib.auth.models import User
from rest_framework import serializers

from expenses.serializers import UserSerializer

from .models import Balance


class BalanceSerializer(serializers.ModelSerializer):
    user_1 = UserSerializer(read_only=True)
    user_2 = UserSerializer(read_only=True)

    class Meta:
        model = Balance
        fields = ["id", "user_1", "user_2", "balance"]

    def validate(self, data):
        if data["user_1"] == data["user_2"]:
            raise serializers.ValidationError("Users cannot be the same.")
        return data
