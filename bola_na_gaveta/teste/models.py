from django.db import models
from django.contrib.auth.models import User

#Victor - Perfis Gerenciador e Jogador
class Perfil(models.Model):
    TIPOS_USUARIO = (
        ('gerenciador', 'Gerenciador'),
        ('jogador', 'Jogador'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_usuario_display()}"

class Competicao(models.Model):
    nome = models.CharField(max_length=100)  
    numero_de_times = models.PositiveIntegerField()  
    local = models.CharField(max_length=100)  

    def __str__(self):
        return self.nome
    

class Time(models.Model):
    nome = models.CharField(max_length=100)
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE, related_name='times')
    jogadores = models.ManyToManyField(User)

    def __str__(self):
        return self.nome
    
# Create your models here.
