from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs de autenticação (login, logout, etc.)
    path('contas/', include('django.contrib.auth.urls')), 
    
    # URLs principais do app 'tarefas'
    path('', include('tarefas.urls')), 
]