from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import BankAccount, Transaction
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Gera dados falsos para teste do sistema'

    def add_arguments(self, parser):
        parser.add_argument('--accounts', type=int, default=3, help='Número de contas a serem criadas')
        parser.add_argument('--transactions', type=int, default=50, help='Número de transações por conta')

    def handle(self, *args, **options):
        # Criar usuário de teste se não existir
        username = 'teste'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': 'teste@example.com',
                'is_active': True
            }
        )
        if created:
            user.set_password('teste123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Usuário {username} criado com senha: teste123'))
        
        # Lista de bancos para escolha aleatória
        banks = [
            ('Banco do Brasil', '001'),
            ('Bradesco', '237'),
            ('Itaú', '341'),
            ('Santander', '033'),
            ('Caixa', '104'),
            ('Nubank', '260'),
        ]
        
        # Criar contas bancárias
        for i in range(options['accounts']):
            bank = random.choice(banks)
            account = BankAccount.objects.create(
                user=user,
                bank_name=bank[0],
                account_number=f'{bank[1]}-{random.randint(10000, 99999)}-{random.randint(0, 9)}',
                manager_name=f'Gerente {i+1}',
                manager_contact=f'(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}'
            )
            self.stdout.write(self.style.SUCCESS(f'Conta criada: {account.bank_name} - {account.account_number}'))
            
            # Gerar transações para cada conta
            start_date = timezone.now() - timedelta(days=180)
            for j in range(options['transactions']):
                transaction_date = start_date + timedelta(days=random.randint(0, 180))
                transaction_type = random.choice(['C', 'D'])
                value = Decimal(random.uniform(10, 5000)).quantize(Decimal('0.01'))
                
                # Lista de descrições possíveis
                credit_descriptions = [
                    'Salário', 'Transferência Recebida', 'Rendimentos', 'Reembolso',
                    'Venda', 'Aluguel', 'Investimento', 'Depósito'
                ]
                debit_descriptions = [
                    'Supermercado', 'Energia Elétrica', 'Água', 'Internet',
                    'Aluguel', 'Combustível', 'Restaurante', 'Farmácia',
                    'Academia', 'Streaming', 'Transporte', 'Vestuário'
                ]
                
                description = random.choice(credit_descriptions if transaction_type == 'C' else debit_descriptions)
                
                Transaction.objects.create(
                    account=account,
                    date=transaction_date,
                    document=f'DOC{random.randint(100000, 999999)}',
                    description=description,
                    transaction_type=transaction_type,
                    value=value
                )
            
            self.stdout.write(self.style.SUCCESS(f'{options["transactions"]} transações criadas para {account.bank_name}'))
        
        total_accounts = BankAccount.objects.filter(user=user).count()
        total_transactions = Transaction.objects.filter(account__user=user).count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal: {total_accounts} contas e {total_transactions} transações criadas'))
