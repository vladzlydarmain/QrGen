from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from editor.models import QrCode
from userpages.models import Plan, UserMod
from django.shortcuts import get_object_or_404
import datetime

# Create your views here.
def show_profile(request):
    context = {
        "user":{"email":None, "name":None,"plan_info":None,"user_info":None}
    }
    if request.method == "POST":
        if request.POST["button"] == "log out":
            logout(request)
            return redirect("login")

    if request.method == "GET":
        if request.user.is_authenticated:
            name = request.user
            email = request.user.email
            userinfo = UserMod.objects.get(user=User.objects.get(username = name))
            plan = UserMod.objects.get(user=User.objects.get(username = name)).plan
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
            usser = UserMod.objects.get(user=User.objects.get(username=user))
            usser.last_payment = str((datetime.datetime.now()).date())
            usser.plan = plan
            usser.qr_scans = 0
            usser.save()
            return redirect("profile")
    
    response = render(request, "userpages/pay.html", context = context)
    return response

def show_redirect_page(request, qr_pk):
    qrobj = get_object_or_404(QrCode,pk = qr_pk)
    user = UserMod.objects.get(user = qrobj.user.user)
    userplan = user.plan
    user_last_payment = datetime.datetime.strptime(user.last_payment,'%Y-%m-%d')
    date = datetime.date.today()
    if (user_last_payment.month < date.month and date.day == user_last_payment.day and user_last_payment.year <= date.year) or (user_last_payment.month < date.month and date.day > user_last_payment.day) or (user_last_payment.year < date.year):
        return render(request, "userpages/redirect.html", context={
            "code":"Your payment was overdue"
        })

    if user.qr_scans >= userplan.scans and userplan.scans != -1:
        return render(request, "userpages/redirect.html", context={
            "code":"Your amount of scans have been exceeded, please buy new scans on our site"
        })
    user.qr_scans += 1
    user.save()
    return redirect(qrobj.url)