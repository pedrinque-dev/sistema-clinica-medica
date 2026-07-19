from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from accounts.models import CustomUser
from pacientes.models import Paciente
from medicos.models import Medico
from consultas.models import Consulta

@login_required
def dashboard_view(request):
    hoje = timezone.localdate()

    contexto = {
        'hoje': hoje,
    }

    if request.user.perfil == CustomUser.Perfil.MEDICO:
        contexto['consultas_hoje'] = Consulta.objects.select_related('paciente').filter(
            medico=request.user.medico,
            data=hoje,
        )
    else:
        contexto['total_pacientes'] = Paciente.objects.count()
        contexto['total_medicos'] = Medico.objects.count()
        contexto['consultas_hoje'] = Consulta.objects.select_related('paciente', 'medico').filter(
            data=hoje,
        )

    return render(request, 'dashboard/dashboard.html', contexto)
