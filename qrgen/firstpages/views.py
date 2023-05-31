from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Create your views here.

def show_main(request):
    response = render(request, "firstpage/main.html")
    return response

def show_reg(request):
    context = {
        "error_text":""
    }

    if request.method == "POST" and not request.user.is_authenticated:
        user_name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        try:
            User.objects.create_user(username= user_name, password = password, email = email)
        except django.db.utils.IntegrityError:
            context["error_text"] = "User already registered"
            
    response = render(request, "firstpage/reg.html", context = context)
    return response

def show_auth(request):

    response = render(request, "firstpage/auth.html")

    if request.method == "POST" and not request.user.is_authenticated:
        password = request.POST.get("password")
        email = request.POST.get("email")

        user = authenticate(email = email,password = password)
        print(user)
        if user != None:
            return redirect("profile")
        else:
            return redirect("reg")
    return response