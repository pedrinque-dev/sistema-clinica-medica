from django import forms
from .models import Consulta, Prontuario

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data', 'horario', 'status', 'observacoes']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'horario': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        medico = cleaned_data.get('medico')
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')

        if medico and data and horario:
            conflito = Consulta.objects.filter(
                medico=medico,
                data=data,
                horario=horario,
            ).exclude(pk=self.instance.pk)

            if conflito.exists():
                raise forms.ValidationError(
                    'Este médico já possui uma consulta marcada neste dia e horário.'
                )

        return cleaned_data

class ProntuarioForm(forms.ModelForm):
    class Meta:
        model = Prontuario
        fields = ['queixa_principal', 'diagnostico', 'prescricao', 'observacoes']
        widgets = {
            'queixa_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'prescricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
