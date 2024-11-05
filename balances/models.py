from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Balance(models.Model):
    user_1 = models.ForeignKey(
        User, related_name="balance_user_1", on_delete=models.CASCADE
    )
    user_2 = models.ForeignKey(
        User, related_name="balance_user_2", on_delete=models.CASCADE
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_1", "user_2"],
                name="unique_user_pair",
                condition=models.Q(user_1__lt=models.F("user_2")),
            ),
        ]

    def __str__(self):
        return f"Balance between {self.user_1} and {self.user_2}: {self.balance}"
