import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bola_na_gaveta.settings')
django.setup()

from django.contrib.auth.models import User
from teste.models import Perfil 

gerenciadores = Perfil.objects.filter(tipo_usuario='gerenciador')

for perfil in gerenciadores:
    user = perfil.user
    try:
        user.delete()  
        print(f"Gerenciador {user.username} deletado")
    except Exception as e:
        print(f"Erro ao deletar {user.username}: {e}")