from django.urls import path

from .views import TransactionListCreateView, TransactionRetrieveUpdateView

urlpatterns = [
    path(
        "transactions/",
        TransactionListCreateView.as_view(),
        name="transaction-list-create",
    ),
    path(
        "transactions/<int:pk>/",
        TransactionRetrieveUpdateView.as_view(),
        name="transaction-detail",
    ),
]
