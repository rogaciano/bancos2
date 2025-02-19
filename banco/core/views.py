from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import BankAccount, Transaction

# Create your views here.

def dashboard(request):
    accounts = BankAccount.objects.all()
    total_balance = sum(account.get_balance() for account in accounts)
    
    context = {
        'accounts': accounts,
        'total_balance': total_balance,
    }
    return render(request, 'core/dashboard.html', context)

class BankAccountList(ListView):
    model = BankAccount
    template_name = 'core/bankaccount_list.html'
    context_object_name = 'accounts'

class BankAccountCreate(CreateView):
    model = BankAccount
    template_name = 'core/bankaccount_form.html'
    fields = ['bank_name', 'account_number', 'manager_name', 'manager_contact']
    success_url = reverse_lazy('bankaccount-list')

class BankAccountUpdate(UpdateView):
    model = BankAccount
    template_name = 'core/bankaccount_form.html'
    fields = ['bank_name', 'account_number', 'manager_name', 'manager_contact']
    success_url = reverse_lazy('bankaccount-list')

class BankAccountDelete(DeleteView):
    model = BankAccount
    template_name = 'core/bankaccount_confirm_delete.html'
    success_url = reverse_lazy('bankaccount-list')

class TransactionList(ListView):
    model = Transaction
    template_name = 'core/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        account_id = self.kwargs.get('account_id')
        return Transaction.objects.filter(account_id=account_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = get_object_or_404(BankAccount, id=self.kwargs.get('account_id'))
        context['account'] = account
        return context

class TransactionCreate(CreateView):
    model = Transaction
    template_name = 'core/transaction_form.html'
    fields = ['date', 'document', 'description', 'transaction_type', 'value']

    def form_valid(self, form):
        form.instance.account_id = self.kwargs.get('account_id')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('transaction-list', kwargs={'account_id': self.kwargs.get('account_id')})

class TransactionUpdate(UpdateView):
    model = Transaction
    template_name = 'core/transaction_form.html'
    fields = ['date', 'document', 'description', 'transaction_type', 'value']

    def get_success_url(self):
        return reverse_lazy('transaction-list', kwargs={'account_id': self.object.account.id})

class TransactionDelete(DeleteView):
    model = Transaction
    template_name = 'core/transaction_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('transaction-list', kwargs={'account_id': self.object.account.id})
