from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages


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

@login_required
def criar_competicao(request):
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        numero_de_times = request.POST.get("numero_de_times")
        endereco = request.POST.get("endereco_descritivo", "").strip()
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        if not (nome and numero_de_times and endereco and latitude and longitude):
            messages.error(request, "Preencha todos os campos.", extra_tags="danger")
        elif Competicao.objects.filter(nome__iexact=nome).exists():
            messages.error(request, f"Já existe uma competição chamada “{nome}”.", extra_tags="danger")
        else:
            Competicao.objects.create(
                nome=nome,
                numero_de_times=int(numero_de_times),
                endereco_descritivo=endereco,
                latitude=float(latitude),
                longitude=float(longitude),
                gerente=request.user
            )
            return redirect("lista_competicoes")

    return render(request, "criar_competicao.html")


@login_required
def lista_competicoes(request):
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')

    competicoes = Competicao.objects.filter(gerente=request.user)
    return render(request, "lista_competicoes.html", {'competicoes': competicoes})

@login_required
def editar_competicao(request, id):
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')
    
    competicao = get_object_or_404(Competicao, id=id)

    if competicao.gerente != request.user:
        return redirect('lista_competicoes')

    if request.method == 'POST':
        competicao.nome = request.POST.get('nome')
        competicao.numero_de_times = request.POST.get('numero_de_times')
        competicao.endereco_descritivo = request.POST.get('endereco_descritivo')
        competicao.latitude = request.POST.get('latitude')
        competicao.longitude = request.POST.get('longitude')
        competicao.save()
        return redirect('lista_competicoes')

    classificacao = calcular_classificacao(competicao)

    # 👇 Adicione essas duas linhas abaixo
    convites = ConviteCompeticao.objects.filter(competicao=competicao, status='pendente')
    times = Time.objects.filter(competicao=competicao)

    return render(request, 'editar_competicao.html', {
        'competicao': competicao,
        'classificacao': classificacao,
        'convites': convites,
        'times': times
    })



@login_required
def excluir_competicao(request, id):

    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')

    competicao = get_object_or_404(Competicao, id=id)

    if competicao.gerente != request.user:
        return redirect('lista_competicoes')

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
        messages.error(
                    request,
                    f"Limite de times atingido.",
                    extra_tags='danger'
                )

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

from .models import Convite

@login_required
def convidar_jogador(request, time_id):
    time = get_object_or_404(Time, id=time_id)

    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('lista_competicoes')

    if request.method == 'POST':
        jogador_id = request.POST.get('jogador_id')
        if jogador_id:
            jogador = get_object_or_404(User, id=jogador_id)
            
            # Verificar se o usuário tem perfil de jogador
            if hasattr(jogador, 'perfil') and jogador.perfil.tipo_usuario == 'jogador':
                
                # Verificar se já existe convite pendente
                convite_existente = Convite.objects.filter(jogador=jogador, time=time, aceito=None).exists()
                if not convite_existente:
                    Convite.objects.create(jogador=jogador, time=time, enviado_por=request.user)
                    messages.success(request, f"Convite enviado para {jogador.username} com sucesso!")
                else:
                    messages.warning(request, f"Já existe um convite pendente para {jogador.username}.")

    return redirect('editar_times', competicao_id=time.competicao.id)

@login_required
def convites_jogador(request):
    convites = Convite.objects.filter(jogador=request.user, aceito=None)
    return render(request, 'convites_jogador.html', {'convites': convites})

@login_required
def aceitar_convite(request, convite_id):
    convite = get_object_or_404(Convite, id=convite_id, jogador=request.user)

    if request.method == 'POST':
        # Aceita o convite
        convite.aceito = True
        convite.save()

        # Adiciona o jogador ao time
        convite.time.jogadores.add(request.user)

        messages.success(request, f'Você aceitou o convite para o time {convite.time.nome}! Agora você faz parte da competição {convite.time.competicao.nome}.')
        return redirect('competicao_jogador_detalhes', competicao_id=convite.time.competicao.id)

    return redirect('convites_jogador')

@login_required
def recusar_convite(request, convite_id):
    convite = get_object_or_404(Convite, id=convite_id, jogador=request.user)

    if request.method == 'POST':
        convite.aceito = False
        convite.save()
        # FORÇAR a tag para ser "danger" (em vez de "error")
        messages.add_message(request, messages.SUCCESS, f'Você recusou o convite para o time {convite.time.nome}.', extra_tags='danger')

    return redirect('convites_jogador')


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

@login_required
def alternar_finalizacao_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if request.method == 'POST':
        partida.finalizada = not partida.finalizada
        partida.save()

    return redirect('gerenciar_partidas', competicao_id=partida.competicao.id)


#Victor - Partidas Jogador
from datetime import date
from django.utils.timezone import now
from django.db.models import Q
from django.utils import timezone


@login_required
def pagina_jogador(request):
    if request.user.perfil.tipo_usuario != 'jogador':
        return redirect('lista_competicoes')

    times = Time.objects.filter(jogadores=request.user)

    partidas = Partida.objects.filter(
        Q(time_casa__in=times) | Q(time_visitante__in=times),
        data__gte=timezone.now().date(),
        finalizada=False  # só partidas ainda não finalizadas
    ).order_by('data', 'hora')

    return render(request, 'pagina_jogador.html', {
        'times': times,
        'partidas': partidas
    })

@login_required
def historico_partidas_competicao(request, competicao_id):
    if request.user.perfil.tipo_usuario != 'jogador':
        return redirect('lista_competicoes')

    competicao = get_object_or_404(Competicao, id=competicao_id)
    times_jogador = Time.objects.filter(competicao=competicao, jogadores=request.user)

    partidas = Partida.objects.filter(
        competicao=competicao,
        finalizada=True
    ).filter(
        Q(time_casa__in=times_jogador) | Q(time_visitante__in=times_jogador)
    ).order_by('-data', '-hora')

    return render(request, 'historico_partidas.html', {
        'competicao': competicao,
        'partidas': partidas,
    })

#Victor - Estatísticas 
from .models import Partida, Gol, Assistencia, Cartao

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Partida, Gol, Assistencia, Cartao

@login_required
def editar_estatisticas_partida(request, partida_id):
    partida = get_object_or_404(Partida, id=partida_id)

    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')

    jogadores_time_casa = partida.time_casa.jogadores.all()
    jogadores_time_visitante = partida.time_visitante.jogadores.all()

    if request.method == "POST":
        gols_time_casa = int(request.POST.get("gols_time_casa", 0))
        gols_time_visitante = int(request.POST.get("gols_time_visitante", 0))

        # Limpa estatísticas anteriores
        Gol.objects.filter(partida=partida).delete()
        Assistencia.objects.filter(partida=partida).delete()
        Cartao.objects.filter(partida=partida).delete()

        todos_jogadores = list(jogadores_time_casa) + list(jogadores_time_visitante)

        total_gols_casa = 0
        total_gols_visitante = 0

        gols_por_jogador = {}
        assistencias_por_jogador = {}

        for jogador in todos_jogadores:
            gols = int(request.POST.get(f"gols_{jogador.id}", 0))
            assistencias = int(request.POST.get(f"assistencias_{jogador.id}", 0))

            gols_por_jogador[jogador.id] = gols
            assistencias_por_jogador[jogador.id] = assistencias

            if jogador in jogadores_time_casa:
                total_gols_casa += gols
            else:
                total_gols_visitante += gols

        if total_gols_casa != gols_time_casa or total_gols_visitante != gols_time_visitante:
            messages.add_message(request, messages.ERROR,
                f"Erro: O placar informado foi {gols_time_casa}x{gols_time_visitante}, "
                f"mas você atribuiu {total_gols_casa} gols para o time da casa e "
                f"{total_gols_visitante} para o visitante.", extra_tags='danger')
            return render(request, 'editar_estatisticas_partida.html', {
                'partida': partida,
                'jogadores_time_casa': jogadores_time_casa,
                'jogadores_time_visitante': jogadores_time_visitante,
            })

        # Agora validar assistências:
        # Para time da casa
        gols_gerais_casa = sum(gols_por_jogador[j.id] for j in jogadores_time_casa)
        gols_por_jogador_casa = {j.id: gols_por_jogador[j.id] for j in jogadores_time_casa}
        
        total_assistencias_casa = 0
        for jogador in jogadores_time_casa:
            assistencias = assistencias_por_jogador[jogador.id]
            gols_dos_outros = gols_gerais_casa - gols_por_jogador_casa[jogador.id]

            if assistencias > gols_dos_outros:
                messages.add_message(request, messages.ERROR,
                    f"Erro: O jogador {jogador.username} registrou {assistencias} assistências, "
                    f"mas o time teve apenas {gols_dos_outros} gols feitos por outros jogadores.", extra_tags='danger')
                return render(request, 'editar_estatisticas_partida.html', {
                    'partida': partida,
                    'jogadores_time_casa': jogadores_time_casa,
                    'jogadores_time_visitante': jogadores_time_visitante,
                })
            total_assistencias_casa += assistencias

        # Para time visitante
        gols_gerais_visitante = sum(gols_por_jogador[j.id] for j in jogadores_time_visitante)
        gols_por_jogador_visitante = {j.id: gols_por_jogador[j.id] for j in jogadores_time_visitante}

        total_assistencias_visitante = 0
        for jogador in jogadores_time_visitante:
            assistencias = assistencias_por_jogador[jogador.id]
            gols_dos_outros = gols_gerais_visitante - gols_por_jogador_visitante[jogador.id]

            if assistencias > gols_dos_outros:
                messages.add_message(request, messages.ERROR,
                    f"Erro: O jogador {jogador.username} registrou {assistencias} assistências, "
                    f"mas o time teve apenas {gols_dos_outros} gols feitos por outros jogadores.", extra_tags='danger')
                return render(request, 'editar_estatisticas_partida.html', {
                    'partida': partida,
                    'jogadores_time_casa': jogadores_time_casa,
                    'jogadores_time_visitante': jogadores_time_visitante,
                })
            total_assistencias_visitante += assistencias

        # Tudo certo: salvar estatísticas
        partida.gols_time_casa = gols_time_casa
        partida.gols_time_visitante = gols_time_visitante
        partida.finalizada = True
        partida.save()

        for jogador in todos_jogadores:
            gols = gols_por_jogador[jogador.id]
            assistencias = assistencias_por_jogador[jogador.id]
            amarelos = int(request.POST.get(f"amarelos_{jogador.id}", 0))
            vermelhos = int(request.POST.get(f"vermelhos_{jogador.id}", 0))

            for _ in range(gols):
                Gol.objects.create(jogador=jogador, partida=partida)
            for _ in range(assistencias):
                Assistencia.objects.create(jogador=jogador, partida=partida)
            for _ in range(amarelos):
                Cartao.objects.create(jogador=jogador, partida=partida, tipo='amarelo')
            for _ in range(vermelhos):
                Cartao.objects.create(jogador=jogador, partida=partida, tipo='vermelho')

        messages.success(request, "Estatísticas da partida atualizadas com sucesso!")
        return redirect('gerenciar_partidas', competicao_id=partida.competicao.id)

    return render(request, 'editar_estatisticas_partida.html', {
        'partida': partida,
        'jogadores_time_casa': jogadores_time_casa,
        'jogadores_time_visitante': jogadores_time_visitante,
    })

from django.db.models import Count, Q


@login_required
def ranking_jogadores(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)
    jogadores = User.objects.filter(time__competicao=competicao).distinct()

    # Coleta os dados
    gols = Gol.objects.filter(partida__competicao=competicao).values('jogador').annotate(total=Count('id'))
    assistencias = Assistencia.objects.filter(partida__competicao=competicao).values('jogador').annotate(total=Count('id'))
    amarelos = Cartao.objects.filter(partida__competicao=competicao, tipo='amarelo').values('jogador').annotate(total=Count('id'))
    vermelhos = Cartao.objects.filter(partida__competicao=competicao, tipo='vermelho').values('jogador').annotate(total=Count('id'))

    mapa_gols = {x['jogador']: x['total'] for x in gols}
    mapa_assistencias = {x['jogador']: x['total'] for x in assistencias}
    mapa_amarelos = {x['jogador']: x['total'] for x in amarelos}
    mapa_vermelhos = {x['jogador']: x['total'] for x in vermelhos}

    ranking = []
    for jogador in jogadores:
        ranking.append({
            'jogador': jogador,
            'gols': mapa_gols.get(jogador.id, 0),
            'assistencias': mapa_assistencias.get(jogador.id, 0),
            'amarelos': mapa_amarelos.get(jogador.id, 0),
            'vermelhos': mapa_vermelhos.get(jogador.id, 0),
        })

    # Filtro
    filtro = request.GET.get("filtro", "gols")

    if filtro == "assistencias":
        ranking = sorted(ranking, key=lambda x: -x['assistencias'])
    elif filtro == "amarelos":
        ranking = sorted(ranking, key=lambda x: -x['amarelos'])
    elif filtro == "vermelhos":
        ranking = sorted(ranking, key=lambda x: -x['vermelhos'])
    else:
        ranking = sorted(ranking, key=lambda x: -x['gols'])

    return render(request, 'ranking_jogadores.html', {
        'competicao': competicao,
        'ranking': ranking,
        'filtro': filtro
    })


#Tabela de Classificação

from collections import defaultdict
from .models import Partida, Time


def calcular_classificacao(competicao):
    tabela = defaultdict(lambda: {
        'time': None,
        'jogos': 0,
        'vitorias': 0,
        'empates': 0,
        'derrotas': 0,
        'gols_marcados': 0,
        'gols_sofridos': 0,
        'saldo': 0,
        'pontos': 0
    })

    partidas = Partida.objects.filter(competicao=competicao, finalizada=True)

    for partida in partidas:
        casa = partida.time_casa
        visitante = partida.time_visitante
        gols_casa = partida.gols_time_casa
        gols_visitante = partida.gols_time_visitante

        for time, gm, gs in [(casa, gols_casa, gols_visitante), (visitante, gols_visitante, gols_casa)]:
            dados = tabela[time]
            dados['time'] = time
            dados['jogos'] += 1
            dados['gols_marcados'] += gm
            dados['gols_sofridos'] += gs
            dados['saldo'] = dados['gols_marcados'] - dados['gols_sofridos']

        if gols_casa > gols_visitante:
            tabela[casa]['vitorias'] += 1
            tabela[casa]['pontos'] += 3
            tabela[visitante]['derrotas'] += 1
        elif gols_casa < gols_visitante:
            tabela[visitante]['vitorias'] += 1
            tabela[visitante]['pontos'] += 3
            tabela[casa]['derrotas'] += 1
        else:
            tabela[casa]['empates'] += 1
            tabela[visitante]['empates'] += 1
            tabela[casa]['pontos'] += 1
            tabela[visitante]['pontos'] += 1

    return sorted(tabela.values(), key=lambda x: (-x['pontos'], -x['saldo'], -x['gols_marcados']))

@login_required
def tabela_classificacao(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)
    classificacao = calcular_classificacao(competicao)

    return render(request, 'tabela_classificacao.html', {
        'competicao': competicao,
        'classificacao': classificacao,
    })

@login_required
def tabela_classificacao_jogador(request):
    if request.user.perfil.tipo_usuario != 'jogador':
        return redirect('lista_competicoes')

    times = request.user.time_set.all()
    competicoes = set(time.competicao for time in times)

    tabelas = []
    for competicao in competicoes:
        classificacao = calcular_classificacao(competicao)
        tabelas.append({
            'competicao': competicao,
            'classificacao': classificacao
        })

    return render(request, 'tabela_classificacao_jogador.html', {
        'tabelas': tabelas
    })

@login_required
def competicao_jogador_detalhes(request, competicao_id):
    if request.user.perfil.tipo_usuario != 'jogador':
        return redirect('lista_competicoes')

    competicao = get_object_or_404(Competicao, id=competicao_id)

    # Checar se o jogador realmente faz parte da competição
    if not Time.objects.filter(competicao=competicao, jogadores=request.user).exists():
        return redirect('pagina_jogador')

    classificacao = calcular_classificacao(competicao)
    partidas = Partida.objects.filter(competicao=competicao, finalizada=True).order_by('-data', '-hora')

    return render(request, 'competicao_jogador_detalhes.html', {
        'competicao': competicao,
        'classificacao': classificacao,
        'partidas': partidas,
    })

@login_required
def historico_partidas_competicao(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)

    if request.user.perfil.tipo_usuario != 'jogador':
        return redirect('pagina_jogador')

    # Verifica se o jogador participa da competição
    if not Time.objects.filter(competicao=competicao, jogadores=request.user).exists():
        return redirect('pagina_jogador')

    partidas = Partida.objects.filter(competicao=competicao, finalizada=True).order_by('-data', '-hora')

    return render(request, 'historico_partidas_competicao.html', {
        'competicao': competicao,
        'partidas': partidas
    })

@login_required
def meu_perfil(request):
    if request.user.perfil.tipo_usuario != 'jogador':
        return redirect('lista_competicoes')

    perfil = request.user.perfil

    if request.method == 'POST':
        perfil.posicao = request.POST.get('posicao')
        perfil.idade = request.POST.get('idade')
        perfil.peso = request.POST.get('peso')
        perfil.altura = request.POST.get('altura')
        if 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']
        perfil.save()
        messages.success(request, "Perfil atualizado com sucesso!")

    # Estatísticas gerais
    total_gols = Gol.objects.filter(jogador=request.user).count()
    total_assistencias = Assistencia.objects.filter(jogador=request.user).count()
    total_amarelos = Cartao.objects.filter(jogador=request.user, tipo='amarelo').count()
    total_vermelhos = Cartao.objects.filter(jogador=request.user, tipo='vermelho').count()

    # Estatísticas por competição
    competicoes = set(time.competicao for time in request.user.time_set.all())

    estatisticas_por_competicao = []
    for comp in competicoes:
        gols = Gol.objects.filter(partida__competicao=comp, jogador=request.user).count()
        assistencias = Assistencia.objects.filter(partida__competicao=comp, jogador=request.user).count()
        amarelos = Cartao.objects.filter(partida__competicao=comp, jogador=request.user, tipo='amarelo').count()
        vermelhos = Cartao.objects.filter(partida__competicao=comp, jogador=request.user, tipo='vermelho').count()

        estatisticas_por_competicao.append({
            'competicao': comp,
            'gols': gols,
            'assistencias': assistencias,
            'amarelos': amarelos,
            'vermelhos': vermelhos
        })

    return render(request, 'meu_perfil.html', {
        'perfil': perfil,
        'total_gols': total_gols,
        'total_assistencias': total_assistencias,
        'cartoes_amarelos': total_amarelos,
        'cartoes_vermelhos': total_vermelhos,
        'estatisticas_por_competicao': estatisticas_por_competicao,
    })



## Buscar por Competições e Peladas perto do Jogador -Victor

from math import radians, sin, cos, sqrt, atan2

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

@login_required
def buscar_eventos_perto(request):
    if request.user.perfil.tipo_usuario != 'jogador':
        return redirect('pagina_gerente')

    termo = request.GET.get("termo", "").strip()
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    eventos = []

    # 🔍 FILTRO POR TEXTO
    if termo:
        eventos = Competicao.objects.filter(endereco_descritivo__icontains=termo)
        tipo_busca = f'Competições encontradas para "{termo}"'

    # 📍 FILTRO POR DISTÂNCIA
    elif lat and lon:
        lat = float(lat)
        lon = float(lon)
        tipo_busca = "Competições até 10km de você"
        for comp in Competicao.objects.all():
            dist = calcular_distancia_km(lat, lon, comp.latitude, comp.longitude)
            if dist <= 10:
                eventos.append((comp, round(dist, 2)))
        eventos.sort(key=lambda x: x[1])  # ordena pela menor distância

    else:
        tipo_busca = "Nenhum filtro aplicado"

    return render(request, "buscar_eventos_perto.html", {
        "tipo_busca": tipo_busca,
        "termo": termo,
        "lat": lat,
        "lon": lon,
        "eventos": eventos
    })

from .models import ConviteCompeticao

@login_required
def auto_convite_competicao(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)
    
    convite, created = ConviteCompeticao.objects.get_or_create(
        jogador=request.user,
        competicao=competicao
    )

    if not created:
        messages.info(request, "Você já solicitou participação nesta competição.")
    else:
        messages.success(request, "Solicitação enviada com sucesso. Aguarde aprovação do gerente.")

    return redirect('buscar_eventos_perto')

@login_required
def aceitar_convite_interface(request, convite_id):
    convite = get_object_or_404(ConviteCompeticao, id=convite_id)

    # Verifica se o gerente é dono da competição
    if convite.competicao.gerente != request.user:
        messages.error(request, "Você não tem permissão para aceitar este convite.")
        return redirect('editar_competicao', id=convite.competicao.id)

    if request.method == "POST":
        time_id = request.POST.get("time_id")
        if not time_id:
            messages.error(request, "Você deve selecionar um time.")
            return redirect('editar_competicao', id=convite.competicao.id)

        time = get_object_or_404(Time, id=time_id, competicao=convite.competicao)

        # Marca convite como aceito e adiciona o jogador ao time
        convite.status = 'aceito'
        convite.save()

        time.jogadores.add(convite.jogador)

        messages.success(request, f"{convite.jogador.username} foi adicionado ao time {time.nome}.")
        return redirect('editar_competicao', id=convite.competicao.id)

    messages.error(request, "Requisição inválida.")
    return redirect('editar_competicao', id=convite.competicao.id)

@login_required
def recusar_convite_competicao(request, convite_id):
    convite = get_object_or_404(ConviteCompeticao, id=convite_id, competicao__gerente=request.user)
    convite.status = 'recusado'
    convite.save()
    messages.info(request, f"Convite de {convite.jogador.username} recusado.")
    return redirect('editar_competicao', id=convite.competicao.id)
