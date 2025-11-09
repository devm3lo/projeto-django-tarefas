from django.db import models
from django.contrib.auth.models import User # Vamos usar o User do Django

class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    concluida = models.BooleanField(default=False)
    # Ligando a tarefa a um usuário específico
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo