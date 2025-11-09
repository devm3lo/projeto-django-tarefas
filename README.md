# Projeto: Gerenciador de Tarefas (Django)

O objetivo é uma aplicação web simples de "To-Do List" usando o framework Django, atendendo aos requisitos mínimos de 4 histórias de usuário e persistência de dados em um banco SQLite.

---

## Alunos

* **Nomes:** 
* Eduardo Melo - 01706118
* Julia Greicy - 01699517
* Rúbia Evelyn - 01707900
* Italo Guilherme - 01678558

---

## Histórias de Usuário Implementadas

O projeto implementa as seguintes 4 histórias de usuário:

1.  **Cadastro de Usuário:** Como um novo usuário, eu quero me cadastrar na plataforma, para que eu possa ter minha própria conta.
2.  **Autenticação e Listagem:** Como um usuário cadastrado, eu quero fazer login e ver minha lista de tarefas pendentes, para que eu saiba o que preciso fazer.
3.  **Criação de Tarefa:** Como um usuário logado, eu quero adicionar uma nova tarefa à minha lista (informando um título), para que eu possa registrar novos itens.
4.  **Gerenciamento de Tarefas:** Como um usuário logado, eu quero marcar uma tarefa como "concluída" ou "excluir" uma tarefa, para que eu possa gerenciar minha lista.

---

## Como Rodar o Projeto

Para rodar este projeto localmente, siga os passos:

1.  Clone o repositório:
    ```bash
    git clone https://github.com/devm3lo/projeto-django-tarefas
    ```

2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  Instale as dependências:
    ```bash
    pip install django
    ```

4.  Aplique as migrações para criar o banco de dados:
    ```bash
    python manage.py migrate
    ```

5.  Rode o servidor de desenvolvimento:
    ```bash
    python manage.py runserver
    ```

6.  Acesse `http://127.0.0.1:8000/` no seu navegador.