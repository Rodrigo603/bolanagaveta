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
    nome = models.CharField(max_length=100, unique=True)
    numero_de_times = models.PositiveIntegerField()  
    local = models.CharField(max_length=100)  
    gerente = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    

class Time(models.Model):
    nome = models.CharField(max_length=100)
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE, related_name='times')
    jogadores = models.ManyToManyField(User)

    def __str__(self):
        return self.nome
    
class Partida(models.Model):
    competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE, related_name='partidas')
    time_casa = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='partidas_casa')
    time_visitante = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='partidas_visitante')
    data = models.DateField()
    hora = models.TimeField()
    gols_time_casa = models.PositiveIntegerField(default=0)
    gols_time_visitante = models.PositiveIntegerField(default=0)
    finalizada = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.time_casa.nome} vs {self.time_visitante.nome} - {self.data}"
    def vencedor(self):
        if self.gols_time_casa > self.gols_time_visitante:
            return self.time_casa
        elif self.gols_time_visitante > self.gols_time_casa:
            return self.time_visitante
        return None  # Empate
    
class Convite(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='convites_recebidos')
    time = models.ForeignKey('Time', on_delete=models.CASCADE)  # ou onde você definiu Time
    aceito = models.BooleanField(null=True)  # None: pendente, True: aceito, False: recusado
    enviado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='convites_enviados', null=True)

    def __str__(self):
        return f"Convite para {self.jogador.username} - Time {self.time.nome}"



#Estatísticas 

class Gol(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE)
    partida = models.ForeignKey('Partida', on_delete=models.CASCADE)

class Assistencia(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE)
    partida = models.ForeignKey('Partida', on_delete=models.CASCADE)

class Cartao(models.Model):
    CARTAO_CHOICES = [('amarelo', 'Amarelo'), ('vermelho', 'Vermelho')]
    jogador = models.ForeignKey(User, on_delete=models.CASCADE)
    partida = models.ForeignKey('Partida', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=CARTAO_CHOICES)