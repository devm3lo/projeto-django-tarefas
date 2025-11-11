# em tarefas/tests.py (VERSÃO FINAL COM 8 TESTES)

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
        self.client.login(username='userteste', password='123')
        response = self.client.get(reverse('lista_tarefas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Minhas Tarefas Pendentes")

    # --- TESTE 3 ---
    def test_criar_tarefa_com_post_valido(self):
        """ Testa a criação de uma nova tarefa. """
        self.client.login(username='userteste', password='123')
        count_antes = Tarefa.objects.count()
        dados_do_formulario = {'titulo': 'Minha nova tarefa de teste'}

        response = self.client.post(reverse('criar_tarefa'), data=dados_do_formulario)

        count_depois = Tarefa.objects.count()
        self.assertEqual(count_depois, count_antes + 1) # Banco aumentou
        self.assertRedirects(response, reverse('lista_tarefas')) # Redirecionou
        
        nova_tarefa = Tarefa.objects.latest('id')
        self.assertEqual(nova_tarefa.titulo, 'Minha nova tarefa de teste')
        self.assertEqual(nova_tarefa.usuario, self.user) 

    # --- TESTE 4 ---
    def test_concluir_tarefa_pertencente_ao_usuario(self):
        """ Testa se o usuário pode marcar sua própria tarefa como concluída. """
        self.client.login(username='userteste', password='123')
        tarefa = Tarefa.objects.create(titulo='Tarefa para concluir', usuario=self.user, concluida=False)

        response = self.client.get(reverse('concluir_tarefa', args=[tarefa.id]))

        self.assertRedirects(response, reverse('lista_tarefas'))
        tarefa.refresh_from_db() 
        self.assertTrue(tarefa.concluida) # Verifica se ficou True

    # --- TESTE 5 ---
    def test_usuario_nao_pode_concluir_tarefa_de_outro(self):
        """ Testa se o Usuário A NÃO consegue concluir uma tarefa do Usuário B. """
        outro_usuario = User.objects.create_user(username='usuariodono', password='123')
        tarefa_do_outro = Tarefa.objects.create(titulo='Tarefa secreta', usuario=outro_usuario, concluida=False)
        self.client.login(username='userteste', password='123') # Loga como "invasor"

        response = self.client.get(reverse('concluir_tarefa', args=[tarefa_do_outro.id]))

        self.assertEqual(response.status_code, 404) # Deve dar 404 (Não Encontrado)
        tarefa_do_outro.refresh_from_db()
        self.assertFalse(tarefa_do_outro.concluida) # Verifica se continua False

    # --- TESTE 6 ---
    def test_excluir_tarefa_pertencente_ao_usuario(self):
        """ Testa se o usuário pode excluir sua própria tarefa. """
        self.client.login(username='userteste', password='123')
        tarefa = Tarefa.objects.create(titulo='Tarefa para excluir', usuario=self.user)
        self.assertEqual(Tarefa.objects.count(), 1) 

        response = self.client.get(reverse('excluir_tarefa', args=[tarefa.id]))

        self.assertRedirects(response, reverse('lista_tarefas'))
        self.assertEqual(Tarefa.objects.count(), 0) # Verifica se o total é 0

    # --- TESTE 7 (NOVO) ---
    def test_editar_tarefa_com_post_valido(self):
        """
        Testa se o usuário pode editar sua própria tarefa.
        """
        # --- PREPARAÇÃO ---
        self.client.login(username='userteste', password='123')
        tarefa = Tarefa.objects.create(titulo='Título Antigo', usuario=self.user)
        
        # Dados do formulário com o novo título
        dados_do_post = {'titulo': 'Título Novo e Atualizado'}

        # --- AÇÃO ---
        # Simula o envio (POST) do formulário de edição
        response = self.client.post(reverse('editar_tarefa', args=[tarefa.id]), data=dados_do_post)

        # --- VERIFICAÇÃO ---
        self.assertRedirects(response, reverse('lista_tarefas')) # Redirecionou
        
        # Atualiza a variável 'tarefa' com os dados do banco
        tarefa.refresh_from_db()
        
        # VERIFICA se o título mudou
        self.assertEqual(tarefa.titulo, 'Título Novo e Atualizado')

    # --- TESTE 8 (NOVO) ---
    def test_usuario_nao_pode_editar_tarefa_de_outro(self):
        """
        Testa se o Usuário A NÃO consegue editar uma tarefa do Usuário B.
        """
        # --- PREPARAÇÃO ---
        outro_usuario = User.objects.create_user(username='usuariodono', password='123')
        tarefa_do_outro = Tarefa.objects.create(titulo='Título do Outro', usuario=outro_usuario)
        
        # Loga como o "invasor"
        self.client.login(username='userteste', password='123')

        # --- AÇÃO (Tenta acessar a página de edição) ---
        response_get = self.client.get(reverse('editar_tarefa', args=[tarefa_do_outro.id]))
        # --- VERIFICAÇÃO (Deve dar 404) ---
        self.assertEqual(response_get.status_code, 404)

        # --- AÇÃO (Tenta enviar um POST malicioso) ---
        response_post = self.client.post(reverse('editar_tarefa', args=[tarefa_do_outro.id]), data={'titulo': 'Hackeado'})
        # --- VERIFICAÇÃO (Deve dar 404) ---
        self.assertEqual(response_post.status_code, 404)

        # VERIFICAÇÃO FINAL (Garante que o título original não mudou)
        tarefa_do_outro.refresh_from_db()
        self.assertEqual(tarefa_do_outro.titulo, 'Título do Outro')