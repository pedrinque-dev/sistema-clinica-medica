from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.lista_pacientes, name='lista'),
    path('cadastrar/', views.cadastrar_paciente, name='cadastrar'),
    path('<int:pk>/', views.detalhes_paciente, name='detalhes'),
    path('<int:pk>/editar/', views.editar_paciente, name='editar'),
    path('<int:pk>/excluir/', views.excluir_paciente, name='excluir'),
]
