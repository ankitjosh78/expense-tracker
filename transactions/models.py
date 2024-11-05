from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Transaction(models.Model):
    payer = models.ForeignKey(
        User, related_name="transactions_paid", on_delete=models.CASCADE
    )
    payee = models.ForeignKey(
        User, related_name="transactions_received", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payer} paid {self.amount} to {self.payee} on {self.created_at}"
