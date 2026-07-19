from django.urls import path
from . import views

app_name = 'consultas'

urlpatterns = [
    path('', views.lista_consultas, name='lista'),
    path('calendario/', views.calendario_consultas, name='calendario'),
    path('cadastrar/', views.cadastrar_consulta, name='cadastrar'),
    path('<int:pk>/', views.detalhes_consulta, name='detalhes'),
    path('<int:pk>/editar/', views.editar_consulta, name='editar'),
    path('<int:pk>/excluir/', views.excluir_consulta, name='excluir'),
    path('<int:consulta_pk>/prontuario/', views.prontuario_consulta, name='prontuario'),
]
