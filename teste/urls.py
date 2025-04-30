from django.urls import path
from .views import index_view, login_view, cadastro_view, logout_view, criar_competicao 
from .views import lista_competicoes, editar_competicao, excluir_competicao, editar_times 
from .views import pagina_jogador, adicionar_time, editar_time, excluir_time
from .views import convidar_jogador, convites_jogador,aceitar_convite, recusar_convite, remover_jogador_time 
from .views import gerenciar_partidas, adicionar_partida, editar_partida, excluir_partida
from .views import alternar_finalizacao_partida, historico_partidas_competicao, editar_estatisticas_partida, tabela_classificacao
from .views import tabela_classificacao_jogador, competicao_jogador_detalhes, historico_partidas_competicao, ranking_jogadores

urlpatterns = [
    path("", index_view, name="index"), 
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
    path('time/<int:time_id>/convidar/', convidar_jogador, name='convidar_jogador'),
    path('time/<int:time_id>/remover-jogador/<int:jogador_id>/', remover_jogador_time, name='remover_jogador_time'),

    path('pagina_jogador/',pagina_jogador, name='pagina_jogador'),
    path('convites/', convites_jogador, name='convites_jogador'),
    path('convite/<int:convite_id>/aceitar/', aceitar_convite, name='aceitar_convite'),
    path('convite/<int:convite_id>/recusar/', recusar_convite, name='recusar_convite'),
    path('historico/competicao/<int:competicao_id>/', historico_partidas_competicao, name='historico_partidas_competicao'),
    path('jogador/competicao/<int:competicao_id>/', competicao_jogador_detalhes, name='competicao_jogador_detalhes'),
    path('jogador/classificacoes/', tabela_classificacao_jogador, name='tabela_classificacao_jogador'),
    path('jogador/competicao/<int:competicao_id>/historico/', historico_partidas_competicao, name='historico_partidas_competicao'),
    path('competicao/<int:competicao_id>/ranking/', ranking_jogadores, name='ranking_jogadores'),
    
    # URLs para gerenciar partidas
    path('competicao/<int:competicao_id>/partidas/', gerenciar_partidas, name='gerenciar_partidas'),
    path('competicao/<int:competicao_id>/partidas/adicionar/', adicionar_partida, name='adicionar_partida'),
    path('competicao/<int:competicao_id>/classificacao/', tabela_classificacao, name='tabela_classificacao'),
    path('partida/<int:partida_id>/editar/', editar_partida, name='editar_partida'),
    path('partida/<int:partida_id>/excluir/', excluir_partida, name='excluir_partida'),
    path('partida/<int:partida_id>/alternar_finalizacao/', alternar_finalizacao_partida, name='alternar_finalizacao_partida'),
    path('partida/<int:partida_id>/estatisticas/', editar_estatisticas_partida, name='editar_estatisticas_partida'),
]