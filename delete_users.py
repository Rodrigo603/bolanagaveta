
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bola_na_gaveta.settings')  
django.setup()

from django.contrib.auth.models import User


User.objects.all().delete()
print("Todos os usuários foram deletados.")
