from django.urls import path
from .views import (index_view, login_view, cadastro_view, logout_view, criar_competicao, 
                   lista_competicoes, editar_competicao, excluir_competicao, editar_times, 
                   pagina_jogador, adicionar_time, editar_time, excluir_time, 
                   adicionar_jogador_time, remover_jogador_time, 
                   gerenciar_partidas, adicionar_partida, editar_partida, excluir_partida, 
                   alternar_finalizacao_partida, historico_partidas_competicao)  # Importa todas as views

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
    path('time/<int:time_id>/adicionar-jogador/', adicionar_jogador_time, name='adicionar_jogador_time'),
    path('time/<int:time_id>/remover-jogador/<int:jogador_id>/', remover_jogador_time, name='remover_jogador_time'),

    path('pagina_jogador/',pagina_jogador, name='pagina_jogador'),
    path('historico/competicao/<int:competicao_id>/', historico_partidas_competicao, name='historico_partidas_competicao'),
    
    # URLs para gerenciar partidas
    path('competicao/<int:competicao_id>/partidas/', gerenciar_partidas, name='gerenciar_partidas'),
    path('competicao/<int:competicao_id>/partidas/adicionar/', adicionar_partida, name='adicionar_partida'),
    path('partida/<int:partida_id>/editar/', editar_partida, name='editar_partida'),
    path('partida/<int:partida_id>/excluir/', excluir_partida, name='excluir_partida'),
    path('partida/<int:partida_id>/alternar_finalizacao/', alternar_finalizacao_partida, name='alternar_finalizacao_partida'),
]