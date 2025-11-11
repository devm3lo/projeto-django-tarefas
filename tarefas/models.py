from django.db import models
from django.contrib.auth.models import User

class Tarefa(models.Model):
    """Representa uma única tarefa no sistema."""
    
    titulo = models.CharField(max_length=200)
    concluida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)
    
    # Chave estrangeira que liga a Tarefa a um Usuário.
    # Isso garante que cada tarefa tenha um "dono".
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Retorna o título da tarefa como sua representação em string."""
        return self.titulo