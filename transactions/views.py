from django.db import transaction
from rest_framework import generics

from balances.models import Balance

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(payer=self.request.user)


class TransactionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
