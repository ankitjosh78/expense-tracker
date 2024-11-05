from loguru import logger
from rest_framework import generics

from .models import Balance
from .serializers import BalanceSerializer


class BalanceUserListView(generics.ListAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        logger.info(f"User {user} is fetching balances:")
        queryset = queryset.filter(user_1=user) | queryset.filter(user_2=user)
        for balance in queryset:
            logger.info(f"Balance: {balance}")
        return queryset


class BalanceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
