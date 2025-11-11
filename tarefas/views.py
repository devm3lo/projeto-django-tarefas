# --- IMPORTS ---
# (Eu juntei seus imports duplicados para ficar mais limpo)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Tarefa
from .forms import TarefaForm

# --- CLASSE DE CADASTRO ---
# Esta classe começa na borda esquerda
class CadastroView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # Redireciona para o login após cadastrar
    template_name = 'registration/cadastro.html'
# A classe TERMINA AQUI

# --- FUNÇÕES ---
# Note que esta linha começa na borda esquerda, FORA da classe
@login_required 
def lista_tarefas(request):
    # Filtra as tarefas para mostrar APENAS as do usuário logado
    tarefas = Tarefa.objects.filter(usuario=request.user, concluida=False)

    # Renderiza o template com as tarefas
    return render(request, 'tarefas/lista_tarefas.html', {'tarefas': tarefas})

# Esta também começa na borda esquerda
@login_required
def criar_tarefa(request):
    if request.method == 'POST':
        # Pega o título do formulário
        titulo = request.POST.get('titulo')
        # Cria a tarefa associada ao usuário logado
        Tarefa.objects.create(titulo=titulo, usuario=request.user)
        # Redireciona de volta para a lista
        return redirect('lista_tarefas')

    # Se não for POST, apenas redireciona (ou poderia ter um form separado)
    return redirect('lista_tarefas')

# Esta também
@login_required
def concluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    tarefa.concluida = True
    tarefa.save()
    return redirect('lista_tarefas')

# E esta também
@login_required
def excluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    tarefa.delete()
    return redirect('lista_tarefas')

# em tarefas/views.py (no final)

@login_required
def editar_tarefa(request, tarefa_id):
    # 1. Pega a tarefa do banco, garantindo que ela pertence ao usuário logado
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)

    # 2. Verifica se o formulário está sendo enviado (POST)
    if request.method == 'POST':
        # Cria uma instância do form COM os dados enviados (request.POST)
        # E diz a ele qual é a tarefa que estamos editando (instance=tarefa)
        form = TarefaForm(request.POST, instance=tarefa)

        if form.is_valid():
            form.save() # Salva as mudanças no banco de dados
            return redirect('lista_tarefas') # Redireciona para a home

    # 3. Se for o primeiro acesso (GET)
    else:
        # Cria o formulário já preenchido com os dados da tarefa
        form = TarefaForm(instance=tarefa) 

    # 4. Renderiza o template de edição
    return render(request, 'tarefas/editar_tarefa.html', {'form': form, 'tarefa': tarefa})