from django.urls import path
from .views import index_view, login_view, cadastro_view, logout_view,criar_competicao,lista_competicoes  # Importa as views

urlpatterns = [
    path("", index_view, name="index"),  # Página inicial
    path("login/", login_view, name="login"),
    path("cadastro/", cadastro_view, name="cadastro"),
    path("logout/", logout_view, name="logout"),
    path("competicoes/nova", criar_competicao,name="criar_competicao"),
    path("competicoes/", lista_competicoes,name= "lista_competicoes"),
]
