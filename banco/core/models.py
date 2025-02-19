from django.db import models
from django.db.models import Sum

# Create your models here.

class BankAccount(models.Model):
    bank_name = models.CharField('Nome do Banco', max_length=100)
    account_number = models.CharField('Número da Conta', max_length=20)
    manager_name = models.CharField('Nome do Gerente', max_length=100)
    manager_contact = models.CharField('Contato do Gerente', max_length=100)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Data de Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Conta Bancária'
        verbose_name_plural = 'Contas Bancárias'
        ordering = ['bank_name']

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"

    def get_balance(self):
        credits = self.transactions.filter(
            transaction_type='C'
        ).aggregate(total=Sum('value'))['total'] or 0
        
        debits = self.transactions.filter(
            transaction_type='D'
        ).aggregate(total=Sum('value'))['total'] or 0
        
        return credits - debits

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('C', 'Crédito'),
        ('D', 'Débito'),
    ]

    account = models.ForeignKey(
        BankAccount, 
        on_delete=models.CASCADE, 
        related_name='transactions',
        verbose_name='Conta'
    )
    date = models.DateField('Data')
    document = models.CharField('Documento', max_length=50)
    description = models.CharField('Descrição', max_length=200)
    transaction_type = models.CharField(
        'Tipo',
        max_length=1,
        choices=TRANSACTION_TYPES
    )
    value = models.DecimalField('Valor', max_digits=15, decimal_places=2)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - {self.description} - {self.value}"
