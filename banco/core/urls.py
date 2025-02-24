from django.urls import path
from .views import (
    BankAccountList, BankAccountCreate, BankAccountUpdate, BankAccountDelete,
    TransactionList, TransactionCreate, TransactionUpdate, TransactionDelete,
    DeleteTransactionsPeriod, dashboard, import_ofx
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/', BankAccountList.as_view(), name='bankaccount-list'),
    path('accounts/create/', BankAccountCreate.as_view(), name='bankaccount-create'),
    path('accounts/<int:pk>/update/', BankAccountUpdate.as_view(), name='bankaccount-update'),
    path('accounts/<int:pk>/delete/', BankAccountDelete.as_view(), name='bankaccount-delete'),
    path('accounts/<int:account_id>/transactions/', TransactionList.as_view(), name='transaction-list'),
    path('accounts/<int:account_id>/transactions/create/', TransactionCreate.as_view(), name='transaction-create'),
    path('accounts/<int:account_id>/transactions/<int:pk>/update/', TransactionUpdate.as_view(), name='transaction-update'),
    path('accounts/<int:account_id>/transactions/<int:pk>/delete/', TransactionDelete.as_view(), name='transaction-delete'),
    path('accounts/<int:account_id>/transactions/delete-period/', DeleteTransactionsPeriod.as_view(), name='transaction-delete-period'),
    path('accounts/<int:account_id>/import-ofx/', import_ofx, name='import-ofx'),
]
