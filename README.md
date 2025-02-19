# Sistema de Controle Bancário

Sistema web desenvolvido em Django para controle de contas bancárias e transações financeiras.

## Funcionalidades

- Cadastro de contas bancárias
- Registro de transações (créditos e débitos)
- Importação de arquivos OFX
- Extrato com saldo acumulado
- Filtros por data e descrição
- Ordenação por múltiplos campos
- Exclusão de transações por período

## Tecnologias

- Python 3.12
- Django 5.0
- Bootstrap 5
- Font Awesome
- SQLite

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/rogaciano/bancos2.git
cd bancos2
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

O sistema estará disponível em `http://127.0.0.1:8000/`

## Uso

1. Faça login com seu usuário
2. Cadastre uma conta bancária
3. Adicione transações manualmente ou importe um arquivo OFX
4. Visualize o extrato com saldo acumulado
5. Use os filtros e ordenação para encontrar transações específicas

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
