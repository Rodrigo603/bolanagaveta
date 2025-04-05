from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



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

from .models import Competicao
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
from .models import Time, Competicao

@login_required
def adicionar_time(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)

    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('lista_competicoes')

    if competicao.times.count() >= competicao.numero_de_times:
        return HttpResponse("Limite de times atingido.")

    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            Time.objects.create(nome=nome, competicao=competicao)
            return redirect('editar_times', competicao_id=competicao.id)

    return render(request, 'adicionar_time_crud.html', {'competicao': competicao})

@login_required
def editar_times(request, competicao_id):
    competicao = get_object_or_404(Competicao, id=competicao_id)
    if request.user.perfil.tipo_usuario != 'gerenciador':
        return redirect('pagina_jogador')
    
    times = Time.objects.filter(competicao=competicao)
    return render(request, 'editar_times.html', {'competicao': competicao, 'times': times})

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
def pagina_jogador(request):
    return render(request, 'pagina_jogador.html')