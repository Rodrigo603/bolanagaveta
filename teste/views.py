from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Victor - redireciona os perfis para suas páginas corretas
            if hasattr(user, 'perfil'):
                if user.perfil.tipo_usuario == 'gerenciador':
                    return redirect('lista_competicoes')  
                elif user.perfil.tipo_usuario == 'jogador':
                    return redirect('pagina_jogador')  # Victor - Criei mas ainda precisa desenvolver
        
        else:
            return render(request, "login.html", {"erro": "Usuário ou senha inválidos"})
    return render(request, "login.html")

#Victor 
from .models import Perfil

def cadastro_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        tipo_usuario = request.POST["tipo_usuario"] 

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, "cadastro.html", {"erro": "Usuário já existe"})
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                # Cria o perfil com o tipo de usuário
                Perfil.objects.create(user=user, tipo_usuario=tipo_usuario)
                # Adiciona mensagem de sucesso
                from django.contrib import messages
                messages.success(request, f"Conta criada com sucesso para {username}! Você já pode fazer login.")
                return redirect("login")
        else:
            return render(request, "cadastro.html", {"erro": "As senhas não coincidem"})

    return render(request, "cadastro.html")

def logout_view(request):
    logout(request)
    return redirect("login")


from django.shortcuts import render

def index_view(request):
    return render(request, "index.html")  # Renderiza a página inicial

@login_required # Victor -  Restringe o acesso para cria_competição só para usuário logado
def criar_competicao(request):
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador') # Victor - Se o usuário for jogador, ele é redirecionado para página dele


    if request.method == "POST":
        nome = request.POST.get("nome")
        numero_de_times = request.POST.get("numero_de_times")
        local = request.POST.get("local")

        if nome and numero_de_times and local:
            Competicao.objects.create(
                nome=nome,
                numero_de_times = int(numero_de_times),
                local=local
            )
            return redirect("lista_competicoes")
    return render(request,"criar_competicao.html")

@login_required
def lista_competicoes(request):
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')

    competicoes = Competicao.objects.all()  
    return render(request, "lista_competicoes.html", {'competicoes': competicoes})

@login_required
def editar_competicao(request,id):
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')
    
    competicao = get_object_or_404(Competicao, id=id)

    if request.method == 'POST':
        competicao.nome = request.POST.get('nome')
        competicao.numero_de_times = request.POST.get('numero_de_times')
        competicao.local = request.POST.get('local')
        competicao.save()
        return redirect('lista_competicoes')

    return render(request, 'editar_competicao.html', {'competicao': competicao})

@login_required
def excluir_competicao(request, id):

    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')

    competicao = get_object_or_404(Competicao, id=id)
    if request.method == 'POST':
        competicao.delete()
    return redirect('lista_competicoes')

from django.contrib.auth.models import User
from .models import Time, Competicao, Partida

@login_required
def adicionar_time(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)

    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('lista_competicoes')

    # limite de times
    if competicao.times.count() >= competicao.numero_de_times:
        return HttpResponse("Limite de times atingido.")

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        if nome:
            
            existe = Time.objects.filter(
                competicao=competicao,
                nome__iexact=nome
            ).exists()
            if existe:
                messages.error(
                    request,
                    f"Já existe um time chamado “{nome}” nesta competição.",
                    extra_tags='danger'
                )
            else:
                Time.objects.create(nome=nome, competicao=competicao)
        else:
            messages.error(request, "O nome do time não pode ficar em branco.", extra_tags='danger')


        return redirect('editar_times', competicao_id=competicao.id)

    return render(request, 'adicionar_time_crud.html', {'competicao': competicao})

@login_required
def editar_times(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')
    
    times = Time.objects.filter(competicao=competicao)
    
    # Obter jogadores com perfil de jogador
    jogadores_disponiveis = User.objects.filter(perfil__tipo_usuario='jogador')
    
    return render(request, 'editar_times.html', {
        'competicao': competicao, 
        'times': times,
        'jogadores_disponiveis': jogadores_disponiveis
    })

@login_required
def editar_time(request, time_id):
    time = get_object_or_404(Time, id=time_id)
    competicao = time.competicao

    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('lista_competicoes')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            time.nome = nome
            time.save()
            return redirect('editar_times', competicao_id=competicao.id)

    return render(request, 'editar_time.html', {'time': time, 'competicao': competicao})

@login_required
def excluir_time(request, time_id):
    time = get_object_or_404(Time, id=time_id)
    competicao_id = time.competicao.id

    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('lista_competicoes')

    time.delete()
    return redirect('editar_times', competicao_id=competicao_id)

@login_required
def adicionar_jogador_time(request, time_id):
    time = get_object_or_404(Time, id=time_id)
    
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('lista_competicoes')
    
    if request.method == 'POST':
        jogador_id = request.POST.get('jogador_id')
        if jogador_id:
            jogador = get_object_or_404(User, id=jogador_id)
            # Verificar se o usuário tem perfil de jogador
            if hasattr(jogador, 'perfil') and jogador.perfil.tipo_usuario == 'jogador':
                time.jogadores.add(jogador)
                
    return redirect('editar_times', competicao_id=time.competicao.id)

@login_required
def remover_jogador_time(request, time_id, jogador_id):
    time = get_object_or_404(Time, id=time_id)
    
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('lista_competicoes')
    
    jogador = get_object_or_404(User, id=jogador_id)
    time.jogadores.remove(jogador)
    
    return redirect('editar_times', competicao_id=time.competicao.id)

@login_required
def pagina_jogador(request):
    # Verifica se o usuário é um jogador
    if request.user.perfil.tipo_usuario != 'jogador':
        return redirect('lista_competicoes')
    
    # Busca os times do jogador
    times = Time.objects.filter(jogadores=request.user)
    
    return render(request, 'pagina_jogador.html', {'times': times})


# Funções movidas de views_partidas.py
@login_required
def gerenciar_partidas(request, competicao_id):
    """View para listar e gerenciar partidas de uma competição"""
    competicao = get_object_or_404(Competicao, id=competicao_id)
    
    # Verificar se o usuário é gerenciador
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')
    
    # Obter times da competição
    times = Time.objects.filter(competicao=competicao)
    
    # Obter partidas da competição
    partidas = Partida.objects.filter(competicao=competicao).order_by('data', 'hora')
    
    return render(request, 'gerenciar_partidas.html', {
        'competicao': competicao,
        'times': times,
        'partidas': partidas
    })

@login_required
def adicionar_partida(request, competicao_id):
    """View para adicionar uma nova partida"""
    competicao = get_object_or_404(Competicao, id=competicao_id)
    
    # Verificar se o usuário é gerenciador
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')
    
    if request.method == 'POST':
        time_casa_id = request.POST.get('time_casa')
        time_visitante_id = request.POST.get('time_visitante')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        
        # Validar dados
        if time_casa_id and time_visitante_id and data and hora:
            # Verificar se os times são diferentes
            if time_casa_id != time_visitante_id:
                time_casa = get_object_or_404(Time, id=time_casa_id)
                time_visitante = get_object_or_404(Time, id=time_visitante_id)
                
                # Criar a partida
                Partida.objects.create(
                    competicao=competicao,
                    time_casa=time_casa,
                    time_visitante=time_visitante,
                    data=data,
                    hora=hora
                )
                
                return redirect('gerenciar_partidas', competicao_id=competicao.id)
    
    # Redirecionar para a página de gerenciamento de partidas
    return redirect('gerenciar_partidas', competicao_id=competicao.id)

@login_required
def editar_partida(request, partida_id):
    """View para editar uma partida existente"""
    partida = get_object_or_404(Partida, id=partida_id)
    competicao = partida.competicao
    
    # Verificar se o usuário é gerenciador
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')
    
    # Obter times da competição
    times = Time.objects.filter(competicao=competicao)
    
    if request.method == 'POST':
        time_casa_id = request.POST.get('time_casa')
        time_visitante_id = request.POST.get('time_visitante')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        
        # Validar dados
        if time_casa_id and time_visitante_id and data and hora:
            # Verificar se os times são diferentes
            if time_casa_id != time_visitante_id:
                time_casa = get_object_or_404(Time, id=time_casa_id)
                time_visitante = get_object_or_404(Time, id=time_visitante_id)
                
                # Atualizar a partida
                partida.time_casa = time_casa
                partida.time_visitante = time_visitante
                partida.data = data
                partida.hora = hora
                partida.save()
                
                return redirect('gerenciar_partidas', competicao_id=competicao.id)
    
    return render(request, 'editar_partida.html', {
        'partida': partida,
        'times': times
    })

@login_required
def excluir_partida(request, partida_id):
    """View para excluir uma partida"""
    partida = get_object_or_404(Partida, id=partida_id)
    competicao_id = partida.competicao.id
    
    # Verificar se o usuário é gerenciador
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')
    
    if request.method == 'POST':
        partida.delete()
    
    return redirect('gerenciar_partidas', competicao_id=competicao_id)
