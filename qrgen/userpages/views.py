from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate
from editor.models import QrCode
from userpages.models import Plan, UserMod
from django.shortcuts import get_object_or_404
import datetime

def check_code(request):
    if 'code' in request.session:
        return request.session["code"]
    else:
        return " "

# Create your views here.
def show_profile(request):
    context = {
        "user":{"email":None, "name":None,"plan_info":None,"user_info":None},
        "code":f"{check_code(request)}"
    }
    if request.method == "POST":
        if request.POST["button"] == "log out":
            logout(request)
            return redirect("login")
        if request.POST["button"] == "endplan":
            form = request.POST
            user = UserMod.objects.get(user= User.objects.get(username=request.user))
            if form["password"] == form["confirm password"] and authenticate(username = request.user, password = form["password"]) != None:
                plan = Plan.objects.get(plantype="Free")
                user.plan = plan
                user.save()
                request.session["code"] = ' '
            else:
                request.session["code"] = "Паролі не співпадають або пароль не вірний"
            return redirect("profile")

    if request.method == "GET":
        if request.user.is_authenticated:
            name = request.user
            email = request.user.email
            userinfo = UserMod.objects.get(user=User.objects.get(username = name))
            plan = userinfo.plan
            context["user"]["name"] = name
            context["user"]["email"] = email
            context["user"]["plan_info"] = plan
            context["user"]["user_info"] = userinfo


        else:
            return redirect("login")

    response = render(request, "userpages/profile.html", context=context)
    return response

def show_all_qr(request):

    if not request.user.is_authenticated:
        return redirect("login")

    username = request.user
    user = UserMod.objects.get(user=User.objects.get(username=username))
    
    context = {
        "qr_list": QrCode.objects.filter(user = user)
    }
    response = render(request, "userpages/all_qr.html", context)

    return response

def show_pay(request):
    context = {
        "plan_info":None
    }
    if request.method == "GET":
        if request.user.is_authenticated:
            if "plantype" in request.session:
                context["plan_info"] = Plan.objects.get(plantype=request.session["plantype"])
            else:
                return redirect("main")
        else:
            return redirect("login")
    if request.method == "POST":
        if "plantype" in request.POST:
            user = request.user

            plan = Plan.objects.get(plantype=request.POST["plantype"])
            userobj = UserMod.objects.get(user=User.objects.get(username=user)) #берем обьект модифюзера по юзеру, которого берем по юзернейму
            userobj.last_payment = str(datetime.date.today())
            userobj.plan = plan
            userobj.qr_scans = 0
            userobj.save()
            return redirect("profile")
    
    response = render(request, "userpages/pay.html", context = context)
    return response

def show_redirect_page(request, qr_pk):
    qrobj = get_object_or_404(QrCode,pk = qr_pk)
    user = qrobj.user
    userplan = user.plan
    user_last_payment = datetime.datetime.strptime(user.last_payment,'%Y-%m-%d')
    date = datetime.date.today()
    if (user_last_payment.month < date.month and date.day == user_last_payment.day and user_last_payment.year <= date.year) or (user_last_payment.month < date.month and date.day > user_last_payment.day) or (user_last_payment.year < date.year):
        return render(request, "userpages/redirect.html", context={
            "code":"Your payment was overdue"
        })#проверка на просрочку даты

    if user.qr_scans >= userplan.scans and userplan.scans != -1:
        return render(request, "userpages/redirect.html", context={
            "code":"Your amount of scans have been exceeded, please buy new scans on our site"
        })#проверка на просрочку сканов
    user.qr_scans += 1
    user.save()
    return redirect(qrobj.url)