from qrgen.settings import MEDIA_URL
from .generate_qr import *
from userpages.models import *
from django.shortcuts import render, redirect
from .models import QrCode
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
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
    return form      

def gradiant_check(gradiant, c1, c2, c3, image = None):
    if gradiant == "SolidFillColorMask()":
        gradiant = SolidFillColorMask(c1,c2)
    if gradiant == "RadialGradiantColorMask()":
        gradiant = RadialGradiantColorMask(c1,c2,c3)
    if gradiant == "SquareGradiantColorMask()":
        gradiant = SquareGradiantColorMask(c1,c2,c3)    
    if gradiant == "VerticalGradiantColorMask()":
        gradiant = VerticalGradiantColorMask(c1,c2,c3)
    if gradiant == "HorizontalGradiantColorMask()":
        gradiant = HorizontalGradiantColorMask(c1,c2,c3)
    if gradiant == "ImageColorMask()":
        gradiant = ImageColorMask(image)
        print("Написано же, что не работает, слепарик!")
    return gradiant    


def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def show_editor(request):
    context = {
        "url":None
    }

    if request.method == "GET" and not request.user.is_authenticated:
        return redirect("login")
        
    if request.method == "POST":
        if "load_file" in request.FILES:
            loaded = request.FILES["load_file"]
            print(loaded)
            

        qr_var = request.POST
        back = qr_var["back_color"][1:]#tip uberau hashteg
        first = qr_var["first_color"][1:]
        second = qr_var["second_color"][1:]
        block_form = qr_var["block_form"]
        gradiant_form = qr_var["gradiant_form"]
        # QrCode.addUser_img(image_file)
        block_form = form_check(block_form)
        name = request.user
        user = UserMod.objects.get(user=User.objects.get(username=name))
        print(qr_var)
        url = qr_var['qr_url']
        if not os.path.exists(MEDIA_URL+f"{name}"):
            os.mkdir(MEDIA_URL+f"{name}")
        b1 = hex_to_rgb(back)
        f1 = hex_to_rgb(first)
        s1 = hex_to_rgb(second)
        gradiant_form = gradiant_check(gradiant_form,b1,f1,s1)  
        new_qr = make_qr(qr_data = url, black_form=block_form, gradient = gradiant_form)
        new_qr.save(MEDIA_URL+f"{name}/generated_qr{len(QrCode.objects.filter(user = UserMod.objects.get(user = User.objects.get(username = name))))+1}.jpg")
        final_qr = QrCode.addQr(user = user, url= url, qrcode_path = f"{name}/generated_qr{len(QrCode.objects.filter(user = UserMod.objects.get(user = User.objects.get(username = name))))+1}.jpg")
        context["url"] = final_qr

    respones = render(request, "editor/editor.html", context)
    return respones