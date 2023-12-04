from datetime import timezone
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from .forms import registerForms, loginForm, profileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from .models import UserProfile
from pages.models import question, answer, Tags, saved
from django .db.models import Count



def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
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
                        "error": "Bu kullanıcı adı kullanılıyor lütfen başka oluşturunuz !",
                        "email": email,
                        "form": form,
                    },
                )
            else:
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(
                        username=username,
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


def profile_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    asked_questions = user_profile.user_questions.all().order_by('-votes')
    answered_questions = user_profile.user_answers.all()
    used_tags = user_profile.user_tags.all()


    user_qusetion = question.objects.filter(user=user_profile.user)
    tags = Tags.objects.filter(question__in=user_qusetion)
    order_tags = tags.annotate(que_count=Count('question')).order_by('-que_count')

    
    data = {
        'user_profile': user_profile,
        'asked_questions': asked_questions,
        'asked_questions_count': asked_questions.count(),
        'answered_questions': answered_questions,
        'answered_questions_count': answered_questions.count(),
        'used_tags': used_tags,
        'order_tags': order_tags,
    }
    
    return render(request, 'pages/profile.html', data)




def activity(request):
    user_profile = UserProfile.objects.get(user=request.user)
    asked_questions = user_profile.user_questions.all().order_by('-votes')
    answered_questions = user_profile.user_answers.all().order_by('-votes')

    user_qusetion = question.objects.filter(user=user_profile.user)
    tags = Tags.objects.filter(question__in=user_qusetion)
    order_tags = tags.annotate(que_count=Count('question')).order_by('-que_count')


    que_votes = sum(asked_questions.values_list('votes', flat=True))
    ans_votes = sum(answered_questions.values_list('votes', flat=True))
    all_votes = que_votes + ans_votes

    
    data = {
        'user_profile': user_profile,
        'asked_questions': asked_questions,
        'answered_questions': answered_questions,
        'order_tags': order_tags,
        'all_votes': all_votes,
        'que_votes': que_votes,
        'ans_votes': ans_votes,
    }
    
    return render(request, 'pages/activity.html', data)    

   



    
def answers_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    answered_questions = user_profile.user_answers.all().order_by('-votes')

    data = {
        'user_profile': user_profile,
        'answered_questions': answered_questions,
        'answered_questions_count': answered_questions.count(),
        }
    return render(request, 'pages/answers_page.html', data)





def questions_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    asked_questions = user_profile.user_questions.all().order_by('-votes')

    asked_questions = asked_questions.annotate(ans_count=Count('answer'))


    data = {
        'user_profile': user_profile,
        'asked_questions': asked_questions,
        'asked_questions_count': asked_questions.count(),
    }

    return render(request, 'pages/profile_guestions.html', data)




def tags_page(request):
    user_profile = UserProfile.objects.get(user=request.user)

    user_qusetion = question.objects.filter(user=user_profile.user)
    tags = Tags.objects.filter(question__in=user_qusetion)
    order_tags = tags.annotate(que_count=Count('question')).order_by('-que_count')


    data = {
        'user_profile': user_profile,
        'order_tags': order_tags,
        'tag_count': order_tags.count(),
    }
    return render(request, 'pages/profile_tags.html', data)







def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user.id)
    if request.method == 'POST':
        form = profileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            username = form.cleaned_data['username']

            if User.objects.filter(username=username).exclude(id=request.user.pk).exists():
                user_profile = UserProfile.objects.get(user=request.user.id)
                form = profileForm()
                return render(request, 'pages/edit_profile.html', {"error": "Bu kullanıcı adı zaten kullanımda.", "form": form, 'user_profile': user_profile,})

            if username:
                user = User.objects.get(username=request.user.username)
                user.username = username
                user.save()
            
            form.save() 
            return redirect('profile_page')
    else:
        form = profileForm(instance=user_profile)
    data = {
        'user_profile': user_profile,
        'form': form
    }
    return render(request, 'pages/edit_profile.html', data)




def saved_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    mySaved = saved.objects.filter(user=request.user.id).select_related('que')
    mySaved_answer_count = mySaved.annotate(answer_count=Count('que__answer'))


    data = {
        'user_profile': user_profile,
        'mySaved': mySaved_answer_count,
        'saved_count': mySaved.count(),
    }
    return render(request, 'pages/profile_saved.html', data)





def is_saved(request, pk):
    que = get_object_or_404(question, id=pk)
    save, created = saved.objects.get_or_create(user=request.user, que=que)

    if not created:
        save.delete()
        return redirect('saved_page')
    return redirect('questionDetail', pk=pk)