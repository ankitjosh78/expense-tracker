from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from balances.models import Balance

from .models import Expense, ExpenseSplit
from .serializers import ExpenseSerializer


class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(created_by=self.request.user)


class ExpenseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
