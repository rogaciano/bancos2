"""
URL configuration for banco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import (
    BankAccountList, BankAccountCreate, BankAccountUpdate, BankAccountDelete,
    TransactionList, TransactionCreate, TransactionUpdate, TransactionDelete,
    DeleteTransactionsPeriod, dashboard, import_ofx,
    UserList, UserCreate, UserUpdate, UserToggleStatus, CustomLogoutView
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    # Usuários
    path('users/', UserList.as_view(), name='user-list'),
    path('users/create/', UserCreate.as_view(), name='user-create'),
    path('users/<int:pk>/update/', UserUpdate.as_view(), name='user-update'),
    path('users/<int:pk>/toggle-status/', UserToggleStatus.as_view(), name='user-toggle-status'),
    path('', include('core.urls')),
]
