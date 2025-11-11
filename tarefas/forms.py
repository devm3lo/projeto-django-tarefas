from django import forms
from .models import Tarefa

class TarefaForm(forms.ModelForm):
    """Formulário para criar e editar uma Tarefa."""
    
    class Meta:
        model = Tarefa
        # Define os campos do modelo que o formulário irá usar
        fields = ['titulo']
        
        # Adiciona classes CSS (Bootstrap) para estilizar o campo no template
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }