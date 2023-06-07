from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from editor.models import QrCode
from userpages.models import Plan, UserMod

# Create your views here.
def show_profile(request):
    context = {
        "user":{"email":None, "name":None,"plan_info":None}
    }
    if request.method == "POST":
        if request.POST["button"] == "log out":
            logout(request)
            return redirect("login")

    if request.method == "GET":
        if request.user.is_authenticated:
            name = request.user
            email = request.user.email
            plan = UserMod.objects.get(user=User.objects.get(username = name)).plan
            context["user"]["name"] = name
            context["user"]["email"] = email
            context["user"]["plan_info"] = plan

        else:
            return redirect("login")

    response = render(request, "userpages/profile.html", context=context)
    return response

def show_all_qr(request):
    
    context = {
        "qr_list": QrCode.objects.all()
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
                # print(context["plan_info"])
            else:
                return redirect("main")
        else:
            return redirect("login")
    if request.method == "POST":
        if "plantype" in request.POST:
            user = request.user

            plan = Plan.objects.get(plantype=request.POST["plantype"])
            usser = UserMod.objects.get(user=User.objects.get(username=user))
            usser.plan = plan
            usser.save()
            return redirect("profile")
    

    response = render(request, "userpages/pay.html", context = context)
    return response