from django.contrib import admin
from .models import Tarefa # <-- IMPORTE SEU MODELO

admin.site.register(Tarefa) # <-- REGISTRE O MODELO AQUI