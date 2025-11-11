# em tarefas/forms.py
from django import forms
from .models import Tarefa

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo'] # O único campo que queremos editar é o 'titulo'

        # (Opcional) Adiciona uma classe do Bootstrap ao campo
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }