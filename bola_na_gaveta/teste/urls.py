from django.urls import path
from .views import index_view, login_view, cadastro_view, logout_view,criar_competicao,lista_competicoes,editar_competicao, excluir_competicao, editar_times, pagina_jogador, adicionar_time, editar_time, excluir_time  # Importa as views

urlpatterns = [
    path("", index_view, name="index"),  # Página inicial
    path("login/", login_view, name="login"),
    path("cadastro/", cadastro_view, name="cadastro"),
    path("logout/", logout_view, name="logout"),
    path("competicoes/nova", criar_competicao,name="criar_competicao"),
    path("competicoes/", lista_competicoes,name= "lista_competicoes"),
    path("competicoes/editar<int:id>/editar",editar_competicao,name="editar_competicao"),
    path("competicoes/excluir<int:id>/excluir",excluir_competicao,name="excluir_competicao"),


    path('competicao/<int:competicao_id>/editar_times/', editar_times, name='editar_times'),
    path('competicao/<int:competicao_id>/times/adicionar/', adicionar_time, name='adicionar_time'),
    path('time/<int:time_id>/editar/', editar_time, name='editar_time'),
    path('time/<int:time_id>/excluir/', excluir_time, name='excluir_time'),


    path('pagina_jogador/',pagina_jogador, name='pagina_jogador'),
]
