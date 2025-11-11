from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Tarefa
from .forms import TarefaForm


class CadastroView(generic.CreateView):
    """View baseada em classe para o cadastro de novos usuários."""
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # Redireciona para o login após cadastrar
    template_name = 'registration/cadastro.html'


@login_required 
def lista_tarefas(request):
    """Exibe a lista de tarefas pendentes do usuário logado."""
    # Filtra as tarefas para mostrar APENAS as do usuário logado e não concluídas.
    tarefas = Tarefa.objects.filter(usuario=request.user, concluida=False)
    return render(request, 'tarefas/lista_tarefas.html', {'tarefas': tarefas})


@login_required
def criar_tarefa(request):
    """Cria uma nova tarefa associada ao usuário logado."""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        # Cria a tarefa já associada ao usuário da requisição
        Tarefa.objects.create(titulo=titulo, usuario=request.user)
        return redirect('lista_tarefas')
    
    # Se for GET, apenas redireciona (o form está na própria lista)
    return redirect('lista_tarefas')


@login_required
def concluir_tarefa(request, tarefa_id):
    """Marca uma tarefa específica como concluída."""
    # O 'get_object_or_404' já filtra pelo 'usuario' para segurança,
    # impedindo que um usuário acesse a tarefa de outro.
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    tarefa.concluida = True
    tarefa.save()
    return redirect('lista_tarefas')


@login_required
def excluir_tarefa(request, tarefa_id):
    """Exclui uma tarefa específica do banco de dados."""
    # Garante que o usuário só possa excluir suas próprias tarefas.
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    tarefa.delete()
    return redirect('lista_tarefas')


@login_required
def editar_tarefa(request, tarefa_id):
    """Exibe um formulário para editar uma tarefa existente."""
    # Garante que o usuário só possa editar suas próprias tarefas.
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)

    if request.method == 'POST':
        # Popula o formulário com os dados enviados (request.POST) e
        # aponta para a instância de tarefa que estamos editando.
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('lista_tarefas')
    else:
        # Se for um acesso GET, cria o formulário já preenchido
        # com os dados atuais da tarefa.
        form = TarefaForm(instance=tarefa) 

    return render(request, 'tarefas/editar_tarefa.html', {'form': form, 'tarefa': tarefa})