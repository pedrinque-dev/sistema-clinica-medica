import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from accounts.decorators import perfil_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from accounts.models import CustomUser
from .models import Consulta, Prontuario
from .forms import ConsultaForm, ProntuarioForm

@login_required
def lista_consultas(request):
    consultas = Consulta.objects.select_related('paciente', 'medico').all()

    if request.user.perfil == CustomUser.Perfil.MEDICO:
        consultas = consultas.filter(medico=request.user.medico)

    paginator = Paginator(consultas, 20)
    numero_pagina = request.GET.get('page')
    consultas_paginadas = paginator.get_page(numero_pagina)

    return render(request, 'consultas/lista_consultas.html', {'consultas': consultas_paginadas})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR, CustomUser.Perfil.RECEPCIONISTA)
def cadastrar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta agendada com sucesso.')
            return redirect('consultas:lista')
    else:
        form = ConsultaForm()

    return render(request, 'consultas/form_consulta.html', {'form': form})

@login_required
def detalhes_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)

    if request.user.perfil == CustomUser.Perfil.MEDICO and consulta.medico != request.user.medico:
        raise PermissionDenied

    return render(request, 'consultas/detalhes_consulta.html', {'consulta': consulta})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR, CustomUser.Perfil.RECEPCIONISTA)
def editar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)

    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta atualizada com sucesso.')
            return redirect('consultas:detalhes', pk=consulta.pk)
    else:
        form = ConsultaForm(instance=consulta)

    return render(request, 'consultas/form_consulta.html', {'form': form, 'consulta': consulta})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR, CustomUser.Perfil.RECEPCIONISTA)
def excluir_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)

    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'Consulta excluída com sucesso.')
        return redirect('consultas:lista')

    return render(request, 'consultas/confirmar_exclusao.html', {'consulta': consulta})

@login_required
def calendario_consultas(request):
    consultas = Consulta.objects.select_related('paciente', 'medico').all()

    if request.user.perfil == CustomUser.Perfil.MEDICO:
        consultas = consultas.filter(medico=request.user.medico)

    dados_consultas = [
        {
            'id': consulta.pk,
            'data': consulta.data.isoformat(),
            'horario': consulta.horario.strftime('%H:%M'),
            'paciente': consulta.paciente.nome_completo,
            'medico': consulta.medico.nome_completo,
            'status': consulta.get_status_display(),
        }
        for consulta in consultas
    ]

    return render(request, 'consultas/calendario.html', {'dados_consultas': dados_consultas})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR, CustomUser.Perfil.MEDICO)
def prontuario_consulta(request, consulta_pk):
    consulta = get_object_or_404(Consulta, pk=consulta_pk)

    if request.user.perfil == CustomUser.Perfil.MEDICO and consulta.medico != request.user.medico:
        raise PermissionDenied

    try:
        prontuario = consulta.prontuario
    except Prontuario.DoesNotExist:
        prontuario = None

    if request.method == 'POST':
        form = ProntuarioForm(request.POST, instance=prontuario)
        if form.is_valid():
            novo_prontuario = form.save(commit=False)
            novo_prontuario.consulta = consulta
            novo_prontuario.save()
            messages.success(request, 'Prontuário salvo com sucesso.')
            return redirect('consultas:detalhes', pk=consulta.pk)
    else:
        form = ProntuarioForm(instance=prontuario)

    return render(request, 'consultas/prontuario.html', {
        'form': form,
        'consulta': consulta,
    })
