from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', views.BankAccountList.as_view(), name='bankaccount-list'),
    path('accounts/create/', views.BankAccountCreate.as_view(), name='bankaccount-create'),
    path('accounts/<int:pk>/update/', views.BankAccountUpdate.as_view(), name='bankaccount-update'),
    path('accounts/<int:pk>/delete/', views.BankAccountDelete.as_view(), name='bankaccount-delete'),
    path('accounts/<int:account_id>/transactions/', views.TransactionList.as_view(), name='transaction-list'),
    path('accounts/<int:account_id>/transactions/create/', views.TransactionCreate.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/update/', views.TransactionUpdate.as_view(), name='transaction-update'),
    path('transactions/<int:pk>/delete/', views.TransactionDelete.as_view(), name='transaction-delete'),
    path('accounts/<int:account_id>/import-ofx/', views.import_ofx, name='import-ofx'),
    path('accounts/<int:account_id>/transactions/delete-period/', 
         views.DeleteTransactionsPeriod.as_view(), 
         name='delete-transactions-period'),
]
