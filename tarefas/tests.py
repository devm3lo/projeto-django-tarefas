from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Tarefa

class TestesPaginaTarefas(TestCase):
    
    def setUp(self):
        """Cria um usuário padrão para ser usado em múltiplos testes."""
        self.user = User.objects.create_user(username='userteste', password='123')

    def test_pagina_lista_tarefas_redireciona_se_usuario_nao_logado(self):
        """Testa se a página inicial redireciona para login se o usuário não estiver logado."""
        response = self.client.get(reverse('lista_tarefas'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/contas/login/?next=/')

    def test_pagina_lista_tarefas_carrega_para_usuario_logado(self):
        """Testa se a página inicial carrega (HTTP 200) para um usuário logado."""
        self.client.login(username='userteste', password='123')
        response = self.client.get(reverse('lista_tarefas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Minhas Tarefas Pendentes")

    def test_criar_tarefa_com_post_valido(self):
        """Testa se um usuário logado pode criar uma nova tarefa via POST."""
        self.client.login(username='userteste', password='123')
        count_antes = Tarefa.objects.count()
        dados_do_formulario = {'titulo': 'Minha nova tarefa de teste'}

        response = self.client.post(reverse('criar_tarefa'), data=dados_do_formulario)

        count_depois = Tarefa.objects.count()
        self.assertEqual(count_depois, count_antes + 1)
        self.assertRedirects(response, reverse('lista_tarefas'))
        
        # Verifica se a tarefa foi criada com os dados corretos e associada ao usuário
        nova_tarefa = Tarefa.objects.latest('id')
        self.assertEqual(nova_tarefa.titulo, 'Minha nova tarefa de teste')
        self.assertEqual(nova_tarefa.usuario, self.user) 

    def test_concluir_tarefa_pertencente_ao_usuario(self):
        """Testa se o usuário pode marcar sua própria tarefa como concluída."""
        self.client.login(username='userteste', password='123')
        tarefa = Tarefa.objects.create(titulo='Tarefa para concluir', usuario=self.user, concluida=False)

        response = self.client.get(reverse('concluir_tarefa', args=[tarefa.id]))

        self.assertRedirects(response, reverse('lista_tarefas'))
        tarefa.refresh_from_db() 
        self.assertTrue(tarefa.concluida)

    def test_usuario_nao_pode_concluir_tarefa_de_outro(self):
        """Testa a segurança: Usuário A não pode concluir uma tarefa do Usuário B."""
        outro_usuario = User.objects.create_user(username='usuariodono', password='123')
        tarefa_do_outro = Tarefa.objects.create(titulo='Tarefa secreta', usuario=outro_usuario, concluida=False)
        
        # Loga como o usuário "invasor"
        self.client.login(username='userteste', password='123')

        response = self.client.get(reverse('concluir_tarefa', args=[tarefa_do_outro.id]))

        # A view deve retornar 404 (Não Encontrado)
        self.assertEqual(response.status_code, 404)
        tarefa_do_outro.refresh_from_db()
        self.assertFalse(tarefa_do_outro.concluida)

    def test_excluir_tarefa_pertencente_ao_usuario(self):
        """Testa se o usuário pode excluir sua própria tarefa."""
        self.client.login(username='userteste', password='123')
        tarefa = Tarefa.objects.create(titulo='Tarefa para excluir', usuario=self.user)
        self.assertEqual(Tarefa.objects.count(), 1) 

        response = self.client.get(reverse('excluir_tarefa', args=[tarefa.id]))

        self.assertRedirects(response, reverse('lista_tarefas'))
        self.assertEqual(Tarefa.objects.count(), 0)

    def test_editar_tarefa_com_post_valido(self):
        """Testa se o usuário pode editar sua própria tarefa via POST."""
        self.client.login(username='userteste', password='123')
        tarefa = Tarefa.objects.create(titulo='Título Antigo', usuario=self.user)
        
        dados_do_post = {'titulo': 'Título Novo e Atualizado'}
        response = self.client.post(reverse('editar_tarefa', args=[tarefa.id]), data=dados_do_post)

        self.assertRedirects(response, reverse('lista_tarefas'))
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.titulo, 'Título Novo e Atualizado')

    def test_usuario_nao_pode_editar_tarefa_de_outro(self):
        """Testa a segurança: Usuário A não pode editar uma tarefa do Usuário B (GET e POST)."""
        outro_usuario = User.objects.create_user(username='usuariodono', password='123')
        tarefa_do_outro = Tarefa.objects.create(titulo='Título do Outro', usuario=outro_usuario)
        
        # Loga como o usuário "invasor"
        self.client.login(username='userteste', password='123')

        # Testa o acesso à página (GET)
        response_get = self.client.get(reverse('editar_tarefa', args=[tarefa_do_outro.id]))
        self.assertEqual(response_get.status_code, 404)

        # Testa o envio malicioso (POST)
        response_post = self.client.post(reverse('editar_tarefa', args=[tarefa_do_outro.id]), data={'titulo': 'Hackeado'})
        self.assertEqual(response_post.status_code, 404)

        # Garante que o título original não mudou
        tarefa_do_outro.refresh_from_db()
        self.assertEqual(tarefa_do_outro.titulo, 'Título do Outro')