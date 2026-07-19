from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from medicos.models import Medico

class CustomUser(AbstractUser):
    class Perfil(models.TextChoices):
        ADMINISTRADOR = 'ADMIN', 'Administrador'
        MEDICO = 'MEDICO', 'Médico'
        RECEPCIONISTA = 'RECEP', 'Recepcionista'

    perfil = models.CharField(
        max_length=10,
        choices=Perfil.choices,
        default=Perfil.RECEPCIONISTA,
    )
    medico = models.OneToOneField(
        Medico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuario',
    )

    def clean(self):
        super().clean()

        if self.perfil == self.Perfil.MEDICO and self.medico is None:
            raise ValidationError({
                'medico': 'Todo usuário com perfil Médico precisa estar vinculado a um Médico.'
            })

        if self.perfil != self.Perfil.MEDICO and self.medico is not None:
            raise ValidationError({
                'medico': 'Apenas usuários com perfil Médico podem estar vinculados a um Médico.'
            })

    def __str__(self):
        return f'{self.username} ({self.get_perfil_display()})'
