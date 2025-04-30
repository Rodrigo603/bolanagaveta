import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bola_na_gaveta.settings')
django.setup()

from django.contrib.auth.models import User
from teste.models import Perfil 

jogadores = Perfil.objects.filter(tipo_usuario='jogador')

for perfil in jogadores:
    user = perfil.user
    try:
        user.delete()  
        print(f"Jogador {user.username} deletado")
    except Exception as e:
        print(f"Erro ao deletar {user.username}: {e}")