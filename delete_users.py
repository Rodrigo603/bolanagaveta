
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bola_na_gaveta.settings')  
django.setup()

from django.contrib.auth.models import User


User.objects.exclude(is_superuser=True).delete()

print("Todos os usuários comuns deletados.")