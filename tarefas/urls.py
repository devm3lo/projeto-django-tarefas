# Em tarefas/urls.py (esta é a versão correta)
from django.urls import path
from . import views

urlpatterns = [
    # URL da Fase 3 (Cadastro)
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    
    # URLs da Fase 4 (Listar e Criar)
    path('', views.lista_tarefas, name='lista_tarefas'),
    path('criar/', views.criar_tarefa, name='criar_tarefa'),

    # URLs da Fase 5 (Concluir e Excluir)
    # (Vamos adicionar estas agora para já deixar pronto)
    path('concluir/<int:tarefa_id>/', views.concluir_tarefa, name='concluir_tarefa'),
    path('excluir/<int:tarefa_id>/', views.excluir_tarefa, name='excluir_tarefa'),
    
    # ... (urls de cadastro, lista, criar, concluir, excluir) ...
    path('excluir/<int:tarefa_id>/', views.excluir_tarefa, name='excluir_tarefa'),

    # --- ADICIONE ESTA LINHA ---
    path('editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
]