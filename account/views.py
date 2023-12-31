from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from stock.forms import userAddForm


# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "account/login_new.html")
    else:
        return render(request, "account/login_new.html")


def user_logout(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":


        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["re-password"]

        if password == password2:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", {"error": "Bu kullanıcı adı daha önce alınmış."})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html", {"error": "Bu email daha önce alınmış."})
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    return redirect("user_login")
        else:
            return render(request, "account/register.html", {"error": "Şifreler eşleşmiyor."})

    else:
        return render(request, "account/register.html")
