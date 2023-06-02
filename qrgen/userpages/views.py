from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from editor.models import QrCode

# Create your views here.
def show_profile(request):
    context = {
        "user":{"email":None, "name":None}
    }

    if request.method == "GET" and request.user.is_authenticated:
        name = request.user
        email = request.user.email
        context["user"]["name"] = name
        context["user"]["email"] = email
    else:
        return redirect("login")
    response = render(request, "userpages/profile.html", context=context)
    return response

def show_all_qr(request):
    
    context = {
        "qr_list": QrCode.objects.all()
    }
    response = render(request, "userpages/all-qr.html", context)

    return response

def show_pay(request):
    response = render(request, "userpages/pay.html")
    return response