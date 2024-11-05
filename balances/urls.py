from django.urls import path

from .views import BalanceUserListView, BalanceRetrieveUpdateView

urlpatterns = [
    path("balances/", BalanceUserListView.as_view(), name="balance-list"),
    path(
        "balances/<int:pk>/", BalanceRetrieveUpdateView.as_view(), name="balance-detail"
    ),
]
