from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from accounts.decorators import perfil_required
from django.core.paginator import Paginator
from accounts.models import CustomUser
from .models import Medico
from .forms import MedicoForm

@login_required
def lista_medicos(request):
    termo_busca = request.GET.get('q', '')

    medicos = Medico.objects.select_related('especialidade').all()

    if termo_busca:
        medicos = medicos.filter(
            Q(nome_completo__icontains=termo_busca) | Q(crm__icontains=termo_busca)
        )

    paginator = Paginator(medicos, 20)
    numero_pagina = request.GET.get('page')
    medicos_paginados = paginator.get_page(numero_pagina)

    return render(request, 'medicos/lista_medicos.html', {
        'medicos': medicos_paginados,
        'termo_busca': termo_busca,
    })

@perfil_required(CustomUser.Perfil.ADMINISTRADOR)
def cadastrar_medico(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médico cadastrado com sucesso.')
            return redirect('medicos:lista')
    else:
        form = MedicoForm()

    return render(request, 'medicos/form_medico.html', {'form': form})

@login_required
def detalhes_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    return render(request, 'medicos/detalhes_medico.html', {'medico': medico})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR)
def editar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)

    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médico atualizado com sucesso.')
            return redirect('medicos:detalhes', pk=medico.pk)
    else:
        form = MedicoForm(instance=medico)

    return render(request, 'medicos/form_medico.html', {'form': form, 'medico': medico})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR)
def excluir_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)

    if request.method == 'POST':
        nome = medico.nome_completo
        medico.delete()
        messages.success(request, f'Médico {nome} excluído com sucesso.')
        return redirect('medicos:lista')

    return render(request, 'medicos/confirmar_exclusao.html', {'medico': medico})
