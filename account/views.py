from django.shortcuts import redirect, render
from .forms import registerForms, loginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        surname = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                form = registerForms()
                return render(
                    request,
                    "pages/register.html",
                    {
                        "error": "Bu kullanıcı adı başkası tarafından kullanılıyor lütfen başka oluşturunuz !",
                        "username": username,
                        "name": first_name,
                        "surname": surname,
                        "email": email,
                        "form": form,
                    },
                )
            else:
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=surname,
                        password=password1,
                        email=email,
                    )
                    user.save()
                    return redirect("login")
                else:
                    form = registerForms()
                    return render(
                        request,
                        "pages/register.html",
                        {
                            "error": "Bu email zaten kayıtlı lütfen başka giriniz !",
                            "username": username,
                            "name": first_name,
                            "surname": surname,
                            "email": email,
                            "form": form,
                        },
                    )

        else:
            form = registerForms()
            return render(
                request,
                "pages/register.html",
                {
                    "error": "Şifreler birbiri ile uyuşmuyor !",
                    "username": username,
                    "name": first_name,
                    "surname": surname,
                    "email": email,
                    "form": form,
                },
            )

    form = registerForms()
    return render(request, "pages/register.html", {"form": form})


def login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("index")
        else:
            form = loginForm()
            return render(
                request,
                "pages/login.html",
                {"error": "Kullanıcı adınızı yada parola bilginizi yanlış girdiniz !", 'form': form},
            )
    form = loginForm()
    return render(request, "pages/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")
