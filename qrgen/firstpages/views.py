from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError
from userpages.models import UserMod, Plan
from userpages.views import check_code
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
        "error_text":f"{check_code(request)}"
    }
    if request.method == "GET" and request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST" and not request.user.is_authenticated:
        user_name = request.POST.get("name")
        password = request.POST.get("password")
        confirm_password = request.POST["confirm password"]
        email = request.POST.get("email")
        
        if user_name == '':
            request.session["code"] = "Ім'я не може бути порожнім!"
            return redirect("reg")
        if len(password) < 6:
            request.session["code"] = "Пароль має бути не менше 6 символів!"
            return redirect("reg")
        if password != confirm_password:
            request.session["code"] = "Паролі не співпадають!"
            return redirect("reg")
        try:
            UserMod.objects.create(user = User.objects.create_user(username = user_name, password = password, email = email), plan=Plan.objects.get(plantype="Free"), last_payment="-",qr_scans=0,qr_amount=0)
            user = authenticate(username = user_name, password = password)
            login(request, user)
            if "plantype" in request.session:
                return redirect("payment")
            else:
                return redirect("profile")
        except IntegrityError:
            context["error_text"] = "Користувач вже зареєстрований"
            
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
            context["error_text"] = "Такого користувача не існує або не вірно вказані данні"
    response = render(request, "firstpage/auth.html", context = context) 
    return response
    