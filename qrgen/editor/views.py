from qrgen.settings import MEDIA_URL
from .generate_qr import *
from userpages.models import *
from django.shortcuts import render, redirect
from .models import QrCode
from django.contrib.auth import authenticate
import os

def form_check(form):
    if form == "SquareModuleDrawer()":
        form = SquareModuleDrawer()
    if form == "CircleModuleDrawer()":
        form = CircleModuleDrawer() 
    if form == "GappedSquareModuleDrawer()":    
        form = GappedSquareModuleDrawer()
    if form == "RoundedModuleDrawer()":
        form = RoundedModuleDrawer()
    if form == "VerticalBarsDrawer()":
        form = VerticalBarsDrawer()
    if form == "HorizontalBarsDrawer()":
        form = HorizontalBarsDrawer()   

def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
# Create your views here.
def show_editor(request):
    context = {
        "url":None
    }

    if request.method == "GET" and not request.user.is_authenticated:
        return redirect("login")
        
    if request.method == "POST":
        qr_var = request.POST
        back = qr_var["back_color"][1:]#tip uberau hashteg
        first = qr_var["first_color"][1:]
        second = qr_var["second_color"][1:]
        block_form = qr_var["block_form"]

        block_form = form_check(block_form)

        name = request.user
        print(qr_var)
        url = qr_var['qr_url']
        if not os.path.exists(MEDIA_URL+f"{name}"):
            os.mkdir(MEDIA_URL+f"{name}")
        b1 = hex_to_rgb(back)
        f1 = hex_to_rgb(first)
        s1 = hex_to_rgb(second)
        
        new_qr = make_qr(qr_data = url, black_form=block_form, gradient = RadialGradiantColorMask(b1,f1,s1))
        new_qr.save(MEDIA_URL+f"{name}/generated_qr{len(UserMod.qr_codes_list)+1}.jpg")
        final_qr = UserMod.addQrCode(url,f"{name}/generated_qr{len(UserMod.qr_codes_list)+1}.jpg")

        
        context["url"] = final_qr

    respones = render(request, "editor/editor.html", context)
    return respones