from django.db import models

class Competicao(models.Model):
    nome = models.CharField(max_length=100)  
    numero_de_times = models.PositiveIntegerField()  
    local = models.CharField(max_length=100)  

    def __str__(self):
        return self.nome
# Create your models here.
