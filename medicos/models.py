from django.db import models

class Especialidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'
        
    def __str__(self):
        return self.nome
    
class Medico(models.Model):
    nome_completo = models.CharField(max_length=150)
    crm = models.CharField(max_length=20, unique=True)
    especialidade = models.ForeignKey(
        Especialidade,
        on_delete=models.PROTECT,
        related_name='medicos'
    )
    telefone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nome_completo']
        
    def __str__(self):
        return f'{self.nome_completo} ({self.especialidade})'
