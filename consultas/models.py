from django.db import models
from pacientes.models import Paciente
from medicos.models import Medico

class Consulta(models.Model):
    class Status(models.TextChoices):
        AGENDADA = 'AGENDADA', 'Agendada'
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'
        REALIZADA = 'REALIZADA', 'Realizada'
        CANCELADA = 'CANCELADA', 'Cancelada'
        
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='consultas',
    )
    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
        related_name='consultas',
    )
    data = models.DateField()
    horario = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.AGENDADA,
    )
    observacoes = models.TextField(blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['data', 'horario']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        
    def __str__(self):
        return f'{self.paciente} com {self.medico} em {self.data} às {self.horario}'
    
class Prontuario(models.Model):
    consulta = models.OneToOneField(
        Consulta,
        on_delete=models.CASCADE,
        related_name='prontuario',
    )
    queixa_principal = models.TextField(blank=True)
    diagnostico = models.TextField(blank=True)
    prescricao = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Prontuário'
        verbose_name_plural = 'Prontuários'

    def __str__(self):
        return f'Prontuário de {self.consulta}'
