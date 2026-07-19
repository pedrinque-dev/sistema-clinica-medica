from django.urls import path
from . import views

app_name = 'medicos'

urlpatterns = [
    path('', views.lista_medicos, name='lista'),
    path('cadastrar/', views.cadastrar_medico, name='cadastrar'),
    path('<int:pk>/', views.detalhes_medico, name='detalhes'),
    path('<int:pk>/editar/', views.editar_medico, name='editar'),
    path('<int:pk>/excluir/', views.excluir_medico, name='excluir'),
]
