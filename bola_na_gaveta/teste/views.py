from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")  # Redireciona para a home (pode ajustar)
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
def criar_competicao(request):
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


def lista_competicoes(request):
    competicoes = Competicao.objects.all()  
    return render(request, "lista_competicoes.html", {'competicoes': competicoes})

def editar_competicao(request,id):

    competicao = get_object_or_404(Competicao, id=id)

    if request.method == 'POST':
        competicao.nome = request.POST.get('nome')
        competicao.numero_de_times = request.POST.get('numero_de_times')
        competicao.local = request.POST.get('local')
        competicao.save()
        return redirect('lista_competicoes')

    return render(request, 'editar_competicao.html', {'competicao': competicao})

def excluir_competicao(request, id):
    competicao = get_object_or_404(Competicao, id=id)
    if request.method == 'POST':
        competicao.delete()
    return redirect('lista_competicoes')