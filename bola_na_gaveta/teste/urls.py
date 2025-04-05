from django.urls import path
from .views import index_view, login_view, cadastro_view, logout_view,criar_competicao,lista_competicoes,editar_competicao, excluir_competicao, adicionar_time  # Importa as views

urlpatterns = [
    path("", index_view, name="index"),  # Página inicial
    path("login/", login_view, name="login"),
    path("cadastro/", cadastro_view, name="cadastro"),
    path("logout/", logout_view, name="logout"),
    path("competicoes/nova", criar_competicao,name="criar_competicao"),
    path("competicoes/", lista_competicoes,name= "lista_competicoes"),
    path("competicoes/editar<int:id>/editar",editar_competicao,name="editar_competicao"),
    path("competicoes/excluir<int:id>/excluir",excluir_competicao,name="excluir_competicao"),
    path('competicao/<int:competicao_id>/adicionar_time/', adicionar_time, name='adicionar_time'),
]
