from django.contrib import admin
from django.urls import path, include # O 'include' é importante

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs de autenticação (login, logout)
    path('contas/', include('django.contrib.auth.urls')), 
    
    # URLs do nosso app 'tarefas'
    path('', include('tarefas.urls')), 
]