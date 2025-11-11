from django.urls import path
from . import views

urlpatterns = [
    # URL de Cadastro
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    
    # URLs do CRUD de Tarefas
    path('', views.lista_tarefas, name='lista_tarefas'),
    path('criar/', views.criar_tarefa, name='criar_tarefa'),
    path('editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
    path('concluir/<int:tarefa_id>/', views.concluir_tarefa, name='concluir_tarefa'),
    path('excluir/<int:tarefa_id>/', views.excluir_tarefa, name='excluir_tarefa'),
]