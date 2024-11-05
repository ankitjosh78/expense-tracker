from django.urls import path

from .views import ExpenseListCreateView, ExpenseRetrieveUpdateView

urlpatterns = [
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list-create"),
    path(
        "expenses/<int:pk>/", ExpenseRetrieveUpdateView.as_view(), name="expense-detail"
    ),
]
