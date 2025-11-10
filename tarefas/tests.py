# em tarefas/tests.py (VERSÃO FINAL COM 5 TESTES)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User # Importamos o User
from .models import Tarefa # Importamos a Tarefa

class TestesPaginaTarefas(TestCase):
    
    # SETUP INICIAL: Cria um usuário que usaremos em vários testes
    def setUp(self):
        self.user = User.objects.create_user(username='userteste', password='123')

    # --- TESTE 1 ---
    def test_pagina_lista_tarefas_redireciona_se_usuario_nao_logado(self):
        """ Testa o redirecionamento se não estiver logado. """
        response = self.client.get(reverse('lista_tarefas'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/contas/login/?next=/')

    # --- TESTE 2 ---
    def test_pagina_lista_tarefas_carrega_para_usuario_logado(self):
        """ Testa o carregamento da página para usuário logado. """
        # Preparação
        self.client.login(username='userteste', password='123')
        # Ação
        response = self.client.get(reverse('lista_tarefas'))
        # Verificação
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Minhas Tarefas Pendentes")

    # --- TESTE 3 ---
    def test_criar_tarefa_com_post_valido(self):
        """ Testa a criação de uma nova tarefa. """
        # Preparação
        self.client.login(username='userteste', password='123')
        count_antes = Tarefa.objects.count()
        dados_do_formulario = {'titulo': 'Minha nova tarefa de teste'}

        # Ação
        response = self.client.post(reverse('criar_tarefa'), data=dados_do_formulario)

        # Verificação
        count_depois = Tarefa.objects.count()
        self.assertEqual(count_depois, count_antes + 1) # Banco aumentou
        self.assertRedirects(response, reverse('lista_tarefas')) # Redirecionou
        
        nova_tarefa = Tarefa.objects.latest('id')
        self.assertEqual(nova_tarefa.titulo, 'Minha nova tarefa de teste')
        self.assertEqual(nova_tarefa.usuario, self.user) # Tarefa é do usuário certo

    # --- TESTE 4 (NOVO) ---
    def test_concluir_tarefa_pertencente_ao_usuario(self):
        """
        Testa se o usuário pode marcar sua própria tarefa como concluída.
        """
        # --- PREPARAÇÃO ---
        # 1. Logar o usuário (já feito no setUp)
        self.client.login(username='userteste', password='123')
        
        # 2. Criar uma tarefa para este usuário
        tarefa = Tarefa.objects.create(
            titulo='Tarefa para concluir', 
            usuario=self.user, 
            concluida=False # Começa como Falsa
        )
        self.assertFalse(tarefa.concluida) # Garante que começou como False

        # --- AÇÃO ---
        # 3. Simular o clique no link 'concluir_tarefa'
        #    (passando o 'id' da tarefa na URL)
        response = self.client.get(reverse('concluir_tarefa', args=[tarefa.id]))

        # --- VERIFICAÇÃO ---
        # 4. Verificar o redirecionamento
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista_tarefas'))

        # 5. Buscar a tarefa no banco de dados DE NOVO
        tarefa.refresh_from_db() 
        
        # 6. VERIFICAR se o status mudou para True
        self.assertTrue(tarefa.concluida)

    # --- TESTE 5 (BÔNUS DE SEGURANÇA) ---
    def test_usuario_nao_pode_concluir_tarefa_de_outro(self):
        """
        Testa se o Usuário A NÃO consegue concluir uma tarefa do Usuário B.
        """
        # --- PREPARAÇÃO ---
        # 1. Criar um segundo usuário (o "dono" da tarefa)
        outro_usuario = User.objects.create_user(username='usuariodono', password='123')
        
        # 2. Criar uma tarefa para o "outro_usuario"
        tarefa_do_outro = Tarefa.objects.create(
            titulo='Tarefa secreta', 
            usuario=outro_usuario, 
            concluida=False
        )
        
        # 3. Logar como o nosso usuário principal (o "invasor")
        self.client.login(username='userteste', password='123')

        # --- AÇÃO ---
        # 4. Tentar acessar a URL para concluir a tarefa do outro usuário
        response = self.client.get(reverse('concluir_tarefa', args=[tarefa_do_outro.id]))

        # --- VERIFICAÇÃO ---
        # 5. VERIFICAR se o Django retornou um erro 404 (Não Encontrado)
        #    (Isso prova que nossa view 'get_object_or_404' funcionou!)
        self.assertEqual(response.status_code, 404)

        # 6. VERIFICAR se a tarefa continua Falsa no banco
        tarefa_do_outro.refresh_from_db()
        self.assertFalse(tarefa_do_outro.concluida)