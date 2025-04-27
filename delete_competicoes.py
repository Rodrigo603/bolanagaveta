
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bola_na_gaveta.settings')  
django.setup()

from teste.models import Competicao


Competicao.objects.all().delete()
print("Todas as competições foram deletadas.")
