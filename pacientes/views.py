from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from accounts.decorators import perfil_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from accounts.models import CustomUser
from .models import Paciente
from .forms import PacienteForm

@login_required
def lista_pacientes(request):
    termo_busca = request.GET.get('q', '')

    if request.user.perfil == CustomUser.Perfil.MEDICO:
        pacientes = Paciente.objects.filter(consultas__medico=request.user.medico).distinct()
    else:
        pacientes = Paciente.objects.all()

    if termo_busca:
        pacientes = pacientes.filter(
            Q(nome_completo__icontains=termo_busca) | Q(cpf__icontains=termo_busca)
        )

    paginator = Paginator(pacientes, 20)
    numero_pagina = request.GET.get('page')
    pacientes_paginados = paginator.get_page(numero_pagina)

    return render(request, 'pacientes/lista_pacientes.html', {
        'pacientes': pacientes_paginados,
        'termo_busca': termo_busca,
    })

@perfil_required(CustomUser.Perfil.ADMINISTRADOR, CustomUser.Perfil.RECEPCIONISTA)
def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente cadastrado com sucesso.')
            return redirect('pacientes:lista')
    else:
        form = PacienteForm()

    return render(request, 'pacientes/form_paciente.html', {'form': form})

@login_required
def detalhes_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.user.perfil == CustomUser.Perfil.MEDICO:
        if not paciente.consultas.filter(medico=request.user.medico).exists():
            raise PermissionDenied

    consultas = paciente.consultas.select_related('medico').all()
    return render(request, 'pacientes/detalhes_paciente.html', {
        'paciente': paciente,
        'consultas': consultas,
    })

@perfil_required(CustomUser.Perfil.ADMINISTRADOR, CustomUser.Perfil.RECEPCIONISTA)
def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente atualizado com sucesso.')
            return redirect('pacientes:detalhes', pk=paciente.pk)
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'pacientes/form_paciente.html', {'form': form, 'paciente': paciente})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR, CustomUser.Perfil.RECEPCIONISTA)
def excluir_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        nome = paciente.nome_completo
        paciente.delete()
        messages.success(request, f'Paciente {nome} excluído com sucesso.')
        return redirect('pacientes:lista')

    return render(request, 'pacientes/confirmar_exclusao.html', {'paciente': paciente})
