from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError
from userpages.models import UserMod, Plan

# Create your views here.

def show_main(request):
    context = {
        "plans":None
    }

    plans = Plan.objects.all()
    context["plans"] = plans
    if request.method == "POST":
        if request.user.is_authenticated:
            request.session["plantype"] = request.POST["plantype"]
            return redirect("payment")
        else:
            request.session["plantype"] = request.POST["plantype"]
            return redirect("login")

    response = render(request, "firstpage/main.html", context = context)
    return response

def show_reg(request):
    context = {
        "error_text":""
    }
    if request.method == "GET" and request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST" and not request.user.is_authenticated:
        user_name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        try:
            UserMod.objects.create(user = User.objects.create_user(username = user_name, password = password, email = email), plan=Plan.objects.get(plantype="Free"))
            user = authenticate(username = user_name, password = password)
            login(request, user)
            if "plantype" in request.session:
                return redirect("payment")
            else:
                return redirect("profile")
        except IntegrityError:
            context["error_text"] = "User already registered"
            
    response = render(request, "firstpage/reg.html", context = context)
    return response

def show_auth(request):
    context = {
        "error_text":""
    }
    if request.method == "GET" and request.user.is_authenticated:
        return redirect("profile")
    if request.method == "POST":
        password = request.POST.get("password")
        name = request.POST.get("name")
        user = authenticate(username = name, password = password)
        if user != None:
            login(request, user)
            if "plantype" in request.session:
                return redirect("payment")
            else:
                return redirect("profile")
        else:
            context["error_text"] = "User wasn't registered or invalid user info"
    response = render(request, "firstpage/auth.html", context = context) 
    return response
    