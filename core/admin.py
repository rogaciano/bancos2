from django.contrib import admin
from .models import BankAccount, Transaction

# Register your models here.

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_number', 'manager_name', 'manager_contact', 'get_balance')
    search_fields = ('bank_name', 'account_number', 'manager_name')
    list_filter = ('bank_name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'account', 'document', 'description', 'transaction_type', 'value')
    list_filter = ('account', 'transaction_type', 'date')
    search_fields = ('document', 'description')
    date_hierarchy = 'date'
