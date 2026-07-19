from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from accounts.decorators import perfil_required
from django.core.paginator import Paginator
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@perfil_required(CustomUser.Perfil.ADMINISTRADOR)
def lista_usuarios(request):
    usuarios = CustomUser.objects.select_related('medico').all()

    paginator = Paginator(usuarios, 20)
    numero_pagina = request.GET.get('page')
    usuarios_paginados = paginator.get_page(numero_pagina)

    return render(request, 'accounts/lista_usuarios.html', {'usuarios': usuarios_paginados})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR)
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário cadastrado com sucesso.')
            return redirect('accounts:lista_usuarios')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/form_usuario.html', {'form': form})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR)
def editar_usuario(request, pk):
    usuario = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário atualizado com sucesso.')
            return redirect('accounts:lista_usuarios')
    else:
        form = CustomUserChangeForm(instance=usuario)

    return render(request, 'accounts/form_usuario.html', {'form': form, 'usuario': usuario})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR)
def trocar_senha_usuario(request, pk):
    usuario = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        form = AdminPasswordChangeForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Senha de {usuario.username} alterada com sucesso.')
            return redirect('accounts:lista_usuarios')
    else:
        form = AdminPasswordChangeForm(usuario)

    if 'usable_password' in form.fields:
        del form.fields['usable_password']

    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})

    return render(request, 'accounts/trocar_senha.html', {'form': form, 'usuario': usuario})

@perfil_required(CustomUser.Perfil.ADMINISTRADOR)
def alternar_status_usuario(request, pk):
    usuario = get_object_or_404(CustomUser, pk=pk)

    if usuario == request.user:
        messages.error(request, 'Você não pode desativar sua própria conta.')
        return redirect('accounts:lista_usuarios')

    if request.method == 'POST':
        usuario.is_active = not usuario.is_active
        usuario.save()

        if usuario.is_active:
            messages.success(request, f'{usuario.username} foi reativado.')
        else:
            messages.success(request, f'{usuario.username} foi desativado.')

        return redirect('accounts:lista_usuarios')

    return render(request, 'accounts/confirmar_status.html', {'usuario': usuario})
