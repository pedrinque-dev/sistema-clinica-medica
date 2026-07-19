from django.db import models

class Paciente(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMININO = 'F', 'Feminino'
        OUTRO = 'O', 'Outro'

    nome_completo = models.CharField(max_length=150)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    endereco = models.CharField(max_length=200, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo
