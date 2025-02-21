from decimal import Decimal
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.db.models import Q, Sum

from .models import BankAccount, Transaction

import xml.etree.ElementTree as ET
import io
import re

@login_required
def dashboard(request):
    accounts = BankAccount.objects.filter(user=request.user)
    total_balance = sum(account.get_balance() for account in accounts)
    
    context = {
        'accounts': accounts,
        'total_balance': total_balance,
    }
    return render(request, 'core/dashboard.html', context)

class BankAccountList(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = 'core/bankaccount_list.html'
    context_object_name = 'accounts'
    ordering = ['bank_name']

    def get_queryset(self):
        queryset = BankAccount.objects.filter(user=self.request.user)
        search = self.request.GET.get('search')
        order = self.request.GET.get('order', 'bank_name')

        if search:
            queryset = queryset.filter(
                Q(bank_name__icontains=search) |
                Q(account_number__icontains=search) |
                Q(manager_name__icontains=search)
            )

        if order in ['bank_name', '-bank_name', 'account_number', '-account_number', 
                    'manager_name', '-manager_name']:
            queryset = queryset.order_by(order)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['order'] = self.request.GET.get('order', 'bank_name')
        return context

class BankAccountCreate(LoginRequiredMixin, CreateView):
    model = BankAccount
    template_name = 'core/bankaccount_form.html'
    fields = ['bank_name', 'account_number', 'manager_name', 'manager_contact']
    success_url = reverse_lazy('bankaccount-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BankAccountUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BankAccount
    template_name = 'core/bankaccount_form.html'
    fields = ['bank_name', 'account_number', 'manager_name', 'manager_contact']
    success_url = reverse_lazy('bankaccount-list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class BankAccountDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BankAccount
    template_name = 'core/bankaccount_confirm_delete.html'
    success_url = reverse_lazy('bankaccount-list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class TransactionList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Transaction
    template_name = 'core/transaction_list.html'
    context_object_name = 'transactions'
    
    def test_func(self):
        account_id = self.kwargs.get('account_id')
        account = get_object_or_404(BankAccount, id=account_id)
        return account.user == self.request.user
    
    def get_queryset(self):
        account_id = self.kwargs.get('account_id')
        queryset = Transaction.objects.filter(account_id=account_id)
        
        # Aplicar ordenação
        order_by = self.request.GET.get('order_by', '-date')
        order_dir = self.request.GET.get('order_dir', 'desc')
        
        # Mapear campos permitidos para ordenação
        allowed_fields = {
            'date': 'date',
            'description': 'description',
            'value': 'value',
        }
        
        # Validar e aplicar ordenação
        if order_by in allowed_fields:
            field = allowed_fields[order_by]
            if order_dir == 'asc':
                queryset = queryset.order_by(field, 'id')
            else:
                queryset = queryset.order_by(f'-{field}', '-id')
        else:
            # Ordenação padrão por data
            queryset = queryset.order_by('-date', '-id')
        
        # Aplicar filtros de busca
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query) |
                Q(document__icontains=search_query)
            )
        
        # Filtrar por data
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        # Calcular saldo acumulado
        transactions = list(queryset)
        running_balance = Decimal('0.00')
        
        for transaction in transactions:
            if transaction.transaction_type == 'C':
                running_balance += transaction.value
            else:
                running_balance -= transaction.value
            transaction.running_balance = running_balance
        
        return transactions
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs.get('account_id')
        account = get_object_or_404(BankAccount, id=account_id)
        
        context.update({
            'account': account,
            'order_by': self.request.GET.get('order_by', 'date'),
            'order_dir': self.request.GET.get('order_dir', 'desc'),
        })
        
        # Calcular totais
        transactions = context['transactions']
        total_credit = sum(t.value for t in transactions if t.transaction_type == 'C')
        total_debit = sum(t.value for t in transactions if t.transaction_type == 'D')
        
        context['total_credit'] = total_credit
        context['total_debit'] = total_debit
        context['balance'] = total_credit - total_debit
        
        return context

class TransactionCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Transaction
    fields = ['date', 'description', 'value', 'transaction_type']
    template_name = 'core/transaction_form.html'
    
    def test_func(self):
        account_id = self.kwargs.get('account_id')
        account = get_object_or_404(BankAccount, id=account_id)
        return account.user == self.request.user

    def form_valid(self, form):
        form.instance.account_id = self.kwargs.get('account_id')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs.get('account_id')
        context['account'] = get_object_or_404(BankAccount, id=account_id)
        return context

    def get_success_url(self):
        return reverse_lazy('transaction-list', kwargs={'account_id': self.kwargs.get('account_id')})

class TransactionUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    fields = ['date', 'description', 'value', 'transaction_type']
    template_name = 'core/transaction_form.html'
    
    def test_func(self):
        transaction = self.get_object()
        return transaction.account.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = self.get_object()
        context['account'] = transaction.account
        return context

    def get_success_url(self):
        transaction = self.get_object()
        return reverse_lazy('transaction-list', kwargs={'account_id': transaction.account.id})

class TransactionDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    template_name = 'core/transaction_confirm_delete.html'

    def test_func(self):
        obj = self.get_object()
        return obj.account.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('transaction-list', kwargs={'account_id': self.object.account.id})

class DeleteTransactionsPeriod(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        account_id = self.kwargs.get('account_id')
        account = get_object_or_404(BankAccount, id=account_id)
        return account.user == self.request.user
    
    def post(self, request, account_id):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if not start_date or not end_date:
            messages.error(request, 'Por favor, selecione as datas inicial e final.')
            return redirect('transaction-list', account_id=account_id)
        
        try:
            # Converter datas
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if start_date > end_date:
                messages.error(request, 'A data inicial não pode ser maior que a data final.')
                return redirect('transaction-list', account_id=account_id)
            
            # Excluir transações do período
            deleted_count = Transaction.objects.filter(
                account_id=account_id,
                date__gte=start_date,
                date__lte=end_date
            ).delete()[0]
            
            messages.success(
                request, 
                f'{deleted_count} transação(ões) excluída(s) com sucesso no período de '
                f'{start_date.strftime("%d/%m/%Y")} a {end_date.strftime("%d/%m/%Y")}.'
            )
            
        except ValueError:
            messages.error(request, 'Formato de data inválido.')
        except Exception as e:
            messages.error(request, f'Erro ao excluir transações: {str(e)}')
        
        return redirect('transaction-list', account_id=account_id)

@login_required
def import_ofx(request, account_id):
    account = get_object_or_404(BankAccount, id=account_id, user=request.user)
    
    if request.method == 'POST':
        ofx_file = request.FILES.get('ofx_file')
        if not ofx_file:
            messages.error(request, 'Por favor, selecione um arquivo OFX para importar.')
            return redirect('transaction-list', account_id=account.id)
        
        try:
            # Ler o arquivo OFX
            content = ofx_file.read()
            
            # Tentar diferentes codificações
            for encoding in ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']:
                try:
                    ofx_content = content.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                messages.error(request, 'Não foi possível ler o arquivo. Erro de codificação.')
                return redirect('transaction-list', account_id=account.id)
            
            # Limpar o conteúdo OFX
            ofx_content = ofx_content.replace('&amp;', '&').replace('\r\n', '\n').replace('\r', '\n')
            
            # Encontrar a parte XML do arquivo
            ofx_start = ofx_content.find('<OFX>') if '<OFX>' in ofx_content else ofx_content.find('<ofx>')
            if ofx_start == -1:
                messages.error(request, 'Arquivo OFX inválido: tag <OFX> não encontrada.')
                return redirect('transaction-list', account_id=account.id)
            
            ofx_content = ofx_content[ofx_start:]
            
            # Converter tags para minúsculas para consistência
            ofx_content = re.sub(r'</?[A-Z]+>', lambda m: m.group(0).lower(), ofx_content)
            
            try:
                # Parse do XML
                root = ET.fromstring(ofx_content)
            except ET.ParseError:
                # Tentar corrigir tags não fechadas
                ofx_content = re.sub(r'<([A-Za-z0-9.]+)>', r'<\1></\1>', ofx_content)
                try:
                    root = ET.fromstring(ofx_content)
                except ET.ParseError as e:
                    messages.error(request, f'Erro ao analisar o arquivo XML: {str(e)}')
                    return redirect('transaction-list', account_id=account.id)
            
            # Encontrar as transações
            transactions_created = 0
            transactions_skipped = 0
            transactions_error = 0
            
            # Procurar por diferentes formatos de transação
            transaction_lists = root.findall('.//banktranlist') + root.findall('.//stmttrn')
            
            if not transaction_lists:
                messages.error(request, 'Nenhuma transação encontrada no arquivo.')
                return redirect('transaction-list', account_id=account.id)
            
            for trans_list in transaction_lists:
                for trans in trans_list.findall('.//stmttrn'):
                    try:
                        # Extrair dados da transação
                        date_text = (
                            trans.findtext('dtposted') or 
                            trans.findtext('dtuser') or 
                            trans.findtext('dtavail')
                        )
                        
                        if not date_text:
                            continue
                        
                        # Converter data
                        try:
                            if len(date_text) >= 8:
                                date = datetime.strptime(date_text[:8], '%Y%m%d').date()
                            else:
                                continue
                        except ValueError:
                            continue
                        
                        # Extrair valor
                        amount_text = trans.findtext('trnamt')
                        if not amount_text:
                            continue
                            
                        try:
                            amount = Decimal(amount_text.replace(',', '.'))
                        except (ValueError, decimal.InvalidOperation):
                            continue
                        
                        # Extrair outros campos
                        description = (
                            trans.findtext('memo') or 
                            trans.findtext('name') or 
                            trans.findtext('trntype') or 
                            'Sem descrição'
                        )[:200]
                        
                        # Gerar ID único
                        transaction_id = (
                            f"{date.strftime('%Y%m%d')}-"
                            f"{abs(float(amount)):.2f}-"
                            f"{hash(description)}"
                        )[:50]
                        
                        # Verificar duplicata
                        if not Transaction.objects.filter(
                            account=account,
                            document=transaction_id,
                            date=date
                        ).exists():
                            # Criar transação
                            Transaction.objects.create(
                                account=account,
                                date=date,
                                document=transaction_id,
                                description=description,
                                transaction_type='C' if amount > 0 else 'D',
                                value=abs(amount)
                            )
                            transactions_created += 1
                        else:
                            transactions_skipped += 1
                            
                    except Exception as e:
                        print(f'Erro ao processar transação: {str(e)}')
                        transactions_error += 1
                        continue
            
            # Mensagem de resultado
            message_parts = []
            if transactions_created > 0:
                message_parts.append(f'{transactions_created} transações importadas com sucesso')
            if transactions_skipped > 0:
                message_parts.append(f'{transactions_skipped} transações já existentes foram ignoradas')
            if transactions_error > 0:
                message_parts.append(f'{transactions_error} transações com erro foram ignoradas')
            
            message = '. '.join(message_parts) + '.'
            
            if transactions_created > 0:
                messages.success(request, message)
            elif transactions_skipped > 0:
                messages.info(request, message)
            else:
                messages.warning(request, message)
                
        except Exception as e:
            print(f'Erro ao processar arquivo OFX: {str(e)}')
            messages.error(request, f'Erro ao processar o arquivo OFX: {str(e)}')
            
    return redirect('transaction-list', account_id=account.id)
