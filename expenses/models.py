from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Expense(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_expenses"
    )
    split_type = models.CharField(
        max_length=10,
        choices=[("equal", "Equal"), ("exact", "Exact"), ("percent", "Percent")],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_by"]),
        ]


class ExpenseSplit(models.Model):
    expense = models.ForeignKey(
        Expense, on_delete=models.CASCADE, related_name="splits"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="expense_splits"
    )
    split_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (
            f"{self.user.username} owes {self.split_value} in {self.split_type} split"
        )
